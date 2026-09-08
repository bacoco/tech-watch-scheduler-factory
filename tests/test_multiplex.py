import json
import unittest
from copy import deepcopy

from support import ROOT
from tech_watch.multiplex import (initial_state, reserve, finish, resolve_dispatch,
                                  validate_registry)


class MultiplexRuntime(unittest.TestCase):
    def registry(self):
        return json.loads((ROOT / 'examples/multiplex-registry.json').read_text())

    def test_three_logical_jobs_validate(self):
        jobs = validate_registry(self.registry())
        self.assertEqual(len(jobs), 3)

    def test_duplicate_job_id_is_rejected(self):
        registry = self.registry()
        registry['jobs'][1]['job_id'] = registry['jobs'][0]['job_id']
        with self.assertRaises(ValueError):
            validate_registry(registry)

    def test_invalid_timezone_is_rejected(self):
        registry = self.registry()
        registry['jobs'][0]['timezone'] = 'Mars/Olympus'
        with self.assertRaises(Exception):
            validate_registry(registry)

    def test_migration_guard_blocks_double_runtime(self):
        registry = self.registry()
        registry['migration']['dedicated_tasks_disabled'] = False
        with self.assertRaises(ValueError):
            reserve(registry, initial_state(), '2026-09-08T09:00:00+02:00')

    def test_single_slot_prevents_double_dispatch(self):
        registry = self.registry(); state = initial_state()
        state, first = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        state2, second = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(first['status'], 'reserved')
        self.assertEqual(second['status'], 'busy')
        self.assertEqual(state2['current']['dispatch_id'], first['dispatch']['dispatch_id'])

    def test_due_jobs_are_consumed_in_stable_order(self):
        registry = self.registry(); state = initial_state()
        state, a = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(a['dispatch']['job_id'], 'example-a.watch')
        state, _ = finish(registry, state, True)
        state, b = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(b['dispatch']['job_id'], 'example-b.watch')

    def test_retry_is_bounded_then_archived_failed(self):
        registry = self.registry(); registry['jobs'] = [registry['jobs'][2]]
        state = initial_state()
        state, first = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(first['dispatch']['attempt'], 1)
        state, retry = finish(registry, state, False)
        self.assertEqual(retry['status'], 'retry')
        state, second = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(second['dispatch']['attempt'], 2)
        state, failed = finish(registry, state, False)
        self.assertEqual(failed['status'], 'failed')
        self.assertIn(second['dispatch']['due_at'], state['failed']['example-c.postmortem'])

    def test_queue_cannot_inject_executable_path(self):
        registry = self.registry(); state = initial_state()
        state, result = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        dispatch = deepcopy(result['dispatch']); dispatch['instructions_path'] = '../evil.md'
        with self.assertRaises(ValueError):
            resolve_dispatch(registry, dispatch)
        resolved = resolve_dispatch(registry, result['dispatch'])
        self.assertEqual(resolved['instructions_path'], 'scheduler-techno/INSTRUCTIONS.md')

    def test_postmortem_guard_is_canonical(self):
        registry = self.registry(); job = registry['jobs'][2]
        self.assertEqual(job['kind'], 'postmortem')
        # The example registry is a runtime fixture; generated packs add the guard.
        # Canonical resolution must never accept a guard injected by the dispatch.
        state = initial_state(); registry['jobs'] = [job]
        state, result = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        dispatch = deepcopy(result['dispatch']); dispatch['guard'] = 'run-anything'
        with self.assertRaises(ValueError):
            resolve_dispatch(registry, dispatch)

    def test_completed_occurrence_is_not_dispatched_again(self):
        registry = self.registry(); registry['jobs'] = [registry['jobs'][0]]
        state = initial_state()
        state, _ = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        state, _ = finish(registry, state, True)
        _, result = reserve(registry, state, '2026-09-08T09:00:00+02:00')
        self.assertEqual(result['status'], 'idle')


if __name__ == '__main__':
    unittest.main()
