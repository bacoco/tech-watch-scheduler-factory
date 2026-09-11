# UPDATE 002 — manual watch requested on 11 September 2026

## Conclusion

This owner-requested manual UPDATE was executed outside the normal Monday cadence, using source repository SHA `111e52313ae2ea070685a3b6bf4761bb0ca07353`.

No material product or runtime change was found since the previous completed UPDATE (`update-2026-09-08-001`, cutoff 2026-09-11T08:12:18+02:00). The current design remains valid:

- periodic multi-source watch remains the primary business cycle;
- event-triggered ChatGPT tasks remain an optional signal lane, not a replacement for periodic research;
- dedicated recovery remains same-occurrence-only and requires positive evidence of a live competing writer before concurrency is declared;
- GitHub Pages activation remains a separate capability from publishing files to the public repository.

No new issue is justified, and the public website projection is a no-op because there is no new material editorial delta.

## q1 — ChatGPT Scheduled Tasks

OpenAI's current Scheduled Tasks documentation still describes event-triggered tasks in Work for supported Gmail, Slack and GitHub pull-request activity. This matches the finding already recorded in issue #7.

**Decision: retain.** Do not create a duplicate issue. Keep periodic research as the fallback and broader discovery path.

## q2 — GitHub Apps and GitHub Pages

GitHub documentation continues to separate repository/app permissions from Pages configuration. Pages can publish from a branch, but activation/configuration requires the relevant repository administration/Pages capability.

The connected GitHub tool in this run could read and write repository content but the direct Pages endpoint was not available through the exposed connector action. The public website repository is still present at commit `5d29dfb8f87c5c596558728ec244199663a1b920`.

**Decision: retain.** Keep `website.status=published_pages_activation_blocked` and do not claim the Pages URL is live.

## q3 — Recovery, retries and idempotency

Fresh research found additional supporting evidence, not a design reversal:

- AWS Durable Execution guidance distinguishes at-least-once replay from at-most-once side-effect handling and recommends stable idempotency keys for retryable external effects.
- AWS's Agentic AI reliability guidance explicitly treats retries without stable idempotency as a high-risk anti-pattern.
- Microsoft Foundry's crash-recovery preview for long-running agents highlights resuming from checkpoints and fencing non-idempotent side effects.
- Temporal material continues to show that worker/process failure recovery depends on durable state and idempotent retryable activities.

These findings strengthen the existing same-occurrence recovery contract but do not require a new issue because the current runtime already resumes the same occurrence, preserves durable progress and forbids stale reservation = concurrency.

**Decision: retain.**

## q4 — Installation and delivery friction

The current two-prompt flow remains unchanged. No new evidence justifies adding another mandatory activation step. Event-triggered signals remain optional, and the public repository / Pages activation distinction remains the main delivery friction.

**Decision: retain.**

## Research and challenge result

The required initial, expansion and challenge movements were executed. Sources actually read include OpenAI, GitHub, AWS, Microsoft and Temporal. Microsoft was used as an expansion source outside the original source list. Challenge research focused on duplicate side effects, unstable retry identity and worker-crash recovery.

No new issue was created because the only actionable event-triggered proposal is already tracked by issue #7 and the new recovery evidence reinforces existing controls rather than exposing a new gap.

## Website consequence

No material public delta was found. Per `WEBSITE.md`, an identical/no-change edition is a no-op. The public website repository remains unchanged at `5d29dfb8f87c5c596558728ec244199663a1b920`.

GitHub Pages activation remains separately unverified/blocked; no live Pages URL is claimed.

## Final status

- watch status: **complete**;
- trigger: **owner-requested manual run**;
- new issues: **0**;
- website files: **no change required**;
- GitHub Pages activation: **blocked separately**;
- baseline: unchanged;
- previous completed update: `update-2026-09-08-001`.
