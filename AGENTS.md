# Agent Instructions

## Model

- `main` is the trusted current product state; development does not happen on it directly.
- Meaningful changes start from a short-lived branch and land via a pull request.
- A GitHub Issue states the human-facing problem/outcome; the task contract (`agent-control/CURRENT_TASK.yaml`) describes only the Agent execution boundary — it does not replace the Issue, the PR, or project history.
- The PR is the primary change/review record. Deterministic CI is separate from the semantic reviewer.
- Default merge is squash; the PR branch is deleted after merge.
- Within the Gate-scoped standing delegation, per-task/per-PR owner authorization is not re-requested. ESCALATE only on genuine human/product/security/architecture boundaries.

## Authority order

1. Repository files and Git diff (including the PR)
2. Machine validation results (deterministic CI)
3. The task contract and current state
4. Chat messages

A chat claim of completion never overrides repository state or failed validation.

## Startup sequence

Before changing files:

1. Read `AGENTS.md`.
2. Read `agent-control/TASK_PROTOCOL.md`.
3. Read `agent-control/CURRENT_TASK.yaml` (execution manifest) when present.
4. Read `state/CURRENT_STATE.yaml` (product/experiment state) when present.
5. Check whether a GitHub Issue / open PR already describes the work.
6. Stop without writes if the contract and state disagree on the active task or status, or the task is not ready.

## Execution rules

- Work on a short-lived branch; never commit product changes directly to `main`.
- Use meaningful commits with lightweight semantic prefixes: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`.
- Modify only `allowed_paths` declared in the contract.
- Never modify or create content under `forbidden_paths`.
- Do not import material from unrelated local repositories.
- This repository is public; commit only content suitable for public disclosure.
- Run every acceptance command and record its actual exit code (deterministic CI covers this).
- Stop after two consecutive tool failures.
- Write the required result file before opening/updating the PR.
- Do not write post-merge lifecycle bookkeeping commits to `main` (GitHub holds merge/review lifecycle).
- Do not start another task automatically unless it is within the standing delegation scope.

## Remote execution boundary

GitHub Actions are GitHub-owned asynchronous execution. The local Agent must not synchronously watch remote workflows (`gh run watch`, polling loops, `sleep` + status reads, watcher daemons). The correct pattern is:

```
push / dispatch / open PR
→ record PR number / run id / head SHA
→ at most one non-blocking status read
→ if the remote workflow is still running, release the foreground
```

Subsequent authoritative GitHub state is re-read only on a new wake/resume/owner interaction. No custom watcher, polling daemon, scheduler, event bus, queue, or controller.
