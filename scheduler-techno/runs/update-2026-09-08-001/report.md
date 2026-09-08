# UPDATE 001 — Self-watch exposed a factory inventory bug

## Conclusion

The end-to-end self-test found a real integration defect after the T0 was frozen: the factory's root repository validator compared every file in the checkout with the package publication whitelist. Installing the legitimate generated `scheduler-techno/` directory into the factory itself would therefore make `tools/check_repository.py` report a publication inventory mismatch.

The fix is now committed on `main` at `14e45a6af7ea3b5d3fdfadddd76c7f91c485dd41`: `scheduler-techno/` is treated as generated runtime state and excluded from the factory package inventory, just like other non-package working directories. The distribution manifest remains unchanged.

## q1 — Scheduled Tasks

Fresh review of OpenAI's current Scheduled Tasks documentation did not reveal a material change requiring a prompt or cadence change. Connected-app permissions and task capacity remain execution-context constraints.

**Decision: retain.** Keep the weekly watch and explicit capability checks.

## q2 — GitHub access and Pages

Fresh GitHub documentation still distinguishes App permissions from selected repository access. GitHub explicitly states that repositories created later by the App are automatically granted to it, reinforcing the T0 lesson from the observed 403. Pages still supports branch publication from the root or `/docs`.

**Decision: retain.** Prefer App-created website repos when allowed; keep `main` + `/(root)` and explicit Pages verification.

## q3 — Runtime reliability

No new evidence invalidates deterministic dispatch, bounded leases, retries, and idempotent effects. The current runtime contracts remain appropriate.

**Decision: retain.** No runtime source change in this update.

## q4 — Installation friction / self-hosting

**Material change.** Self-installation of `scheduler-techno/` conflicted with the factory's own strict package inventory validator.

Root cause: `tools/check_repository.py` treated generated runtime state as distributable factory source.

Fix: add `scheduler-techno` to the validator's skipped runtime/working directories while leaving `tools/publish-files.json` unchanged.

Expected behavior: the factory can watch itself without contaminating or invalidating the package publication inventory.

## Website consequence

This UPDATE becomes a second public edition. The first T0 page remains unchanged; the home and archive are refreshed so the latest edition records the bug found and fixed by the self-test.

## Issues

No issue created: the defect was reproduced, fixed directly, and is now represented by this verified UPDATE run.
