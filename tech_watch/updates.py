"""Commit a complete update receipt locally with an expected previous run."""
from pathlib import Path
from .common import atomic_json, digest, json_text, instant, lock, read_json, require
from .render import validate_pack
from .state import receipt, verify_t0


def record_update(root, data):
    root = Path(root)
    profile = validate_pack(root)
    with lock(root):
        verify_t0(root)
        state = read_json(root / 'state.json')
        require(state['phase'] == 'UPDATE_READY', 'update not eligible')
        receipt(root, data, 'update', profile)
        require(isinstance(data['source_checkpoints'], dict), 'source checkpoints required')
        channels = {c['id'] for c in profile['channels'] if c['mode'] != 'excluded'}
        require(set(data['source_checkpoints']) <= channels, 'unknown/excluded source cursor')
        h = digest(json_text(data).encode())
        current = state['last_completed_update']
        if current and current['run_id'] == data['run_id']:
            require(current['receipt_sha256'] == h, 'same run ID with different receipt')
            return {'status': 'unchanged', 'state': state}
        receipt_path = root / 'runs' / data['run_id'] / 'receipt.json'
        require(not receipt_path.exists(), 'run ID already recorded; reconcile, never overwrite history')
        lower_bound = current['finished_at'] if current else state['baseline']['cutoff_at']
        require(instant(data['finished_at']) >= instant(lower_bound), 'update time moves backwards')
        previous = current['run_id'] if current else None
        require(data['previous_run_id'] == previous, 'stale update parent; reconcile first')
        state['last_completed_update'] = {'run_id': data['run_id'],
            'finished_at': data['finished_at'], 'receipt_sha256': h}
        # Omitted sources keep their cursor. Never erase a blocked source frontier.
        state['source_checkpoints'].update(data['source_checkpoints'])
        atomic_json(root / 'runs' / data['run_id'] / 'receipt.json', data)
        atomic_json(root / 'state.json', state)
    return {'status': 'recorded-locally', 'state': state}
