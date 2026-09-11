# UPDATE 001 — self-watch recovery completed

## Conclusion

This same UPDATE occurrence, first started on 8 September 2026, is now complete rather than replaced by a new cycle. The original material finding remains valid: installing the generated `scheduler-techno/` directory in the factory exposed an inventory-validation bug, fixed by commit `14e45a6af7ea3b5d3fdfadddd76c7f91c485dd41`.

Recovery at pinned source SHA `2ac5979b289013ca5f8913aba7290ba0c43a3dd7` found two additional material facts that belong to this unfinished occurrence:

1. the factory itself now contains a dedicated six-hour recovery path that resumes only the most recent non-terminal occurrence, requires positive live-writer evidence before declaring concurrency, and never starts a new business watch outside cadence;
2. OpenAI now documents event-triggered Scheduled Tasks in ChatGPT Work for supported Gmail, Slack and GitHub pull-request activity. That is useful as an optional signal lane, but it is not a replacement for this watch's periodic multi-source research.

No positive evidence of another live writer or lease was found, so the old incomplete occurrence was safely resumed.

## q1 — Scheduled Tasks

**Material update.** OpenAI's current Scheduled Tasks documentation and the 25 August 2026 release notes document event-triggered tasks tied to app updates, including supported GitHub pull-request activity.

This can reduce detection latency for some repository events, but the supported event surface is narrower than this watch: the factory must still perform periodic open-web research across OpenAI, GitHub, queue/runtime products, community signals and newly discovered sources.

**Decision: retain periodic watch + evaluate an optional event signal.** Issue #7 was created after checking existing open/closed issues and PRs. It proposes a small `periodic | periodic+event` experiment with stable event identity, no extra authority from the trigger, and periodic fallback.

## q2 — GitHub access and Pages

Fresh GitHub documentation continues to separate GitHub App repository selection from API permissions. The public website repository exists, is public, and the connected GitHub integration has write/admin repository permissions.

GitHub Pages still supports branch publication from `main` at `/(root)`, but this execution environment exposes no Pages-settings action. Therefore the watch can publish and verify the public files, but it cannot honestly claim that the Pages site itself is activated or live.

**Decision: retain.** Keep the separate public repository, publish from `main` root, and continue to report Pages activation separately from file delivery.

## q3 — Runtime reliability

**Material update.** Since the original report was written, `main` added and tested a dedicated recovery task. The current runtime contract says:

- recovery runs every six hours;
- it acts only when the latest scheduled watch occurrence is incomplete;
- it resumes exactly that same occurrence;
- an old reservation alone is not concurrency evidence;
- `CONCURRENT_RUN_ACTIVE` requires positive current writer/lease evidence.

That is consistent with the failure models reviewed from AWS, Temporal and Google Cloud: work can become recoverable after a lease/visibility boundary, durable progress should resume rather than restart, duplicate effects must be prevented, and retries must be bounded.

**Decision: retain.** This recovery run is itself a successful exercise of the intended same-occurrence behavior.

## q4 — Installation friction / self-hosting

The original material change remains closed by the existing fix.

Root cause: `tools/check_repository.py` treated generated runtime state as distributable factory source.

Fix: `scheduler-techno/` is excluded from the package inventory validator while the distribution manifest remains unchanged.

**Decision: retain.** No second issue is needed for an already reproduced and fixed defect. The main user flow remains two mini-prompts; the event-triggered idea is optional rather than a new mandatory activation step.

## Research and delivery

Fresh research was rerun for this recovery using all three required movements: initial, expansion and challenge. Sources actually read include OpenAI, GitHub, AWS, Google Cloud and a newly discovered Temporal durable-execution reference. The machine-readable journal is `runs/update-2026-09-08-001/research.json`.

Issue created and reread:

- #7 — `[Veille] Évaluer les tâches événementielles comme voie de signal GitHub optionnelle`.

## Website consequence

This UPDATE is a second public edition. The frozen T0 edition remains unchanged. The website home and archive are refreshed and a distinct edition page is added for UPDATE 001.

Website file publication is verifiable in the public repository. GitHub Pages activation remains a separate blocker because the available connector exposes repository administration but not a Pages-settings mutation or status endpoint. No live Pages URL is claimed.

## Final status

- watch status: **complete**;
- issue delivery: **verified**;
- website files: **published and reread**;
- GitHub Pages activation: **blocked separately**;
- baseline: unchanged;
- occurrence: `update-2026-09-08-001`, resumed and completed without creating a new watch cycle.
