# Agent Instructions

## Authority order

1. Repository files and Git diff
2. Machine validation results
3. Current GitHub task files
4. Chat messages

A chat claim of completion never overrides repository state or failed validation.

## Startup sequence

Before changing files:

1. Read `AGENTS.md`.
2. Read `agent-control/TASK_PROTOCOL.md`.
3. Read `agent-control/CURRENT_TASK.yaml`.
4. Read `state/CURRENT_STATE.yaml` when present.
5. Read the result file identified by `CURRENT_TASK.yaml` or the subject task when present.
6. List all files actually read in the first response.
7. Compare lifecycle claims across task contract, state, and result records.
8. Stop without writes if task contract, current state, and result records disagree on the active task or lifecycle status. Chat or compressed-context claims must never silently resolve contradictions.
9. Confirm the current task boundary in a short structured response.
10. Stop if the task is not `ready` or a declared blocker prevents execution.

## Execution rules

- Execute one `task_id` at a time.
- Modify only `allowed_paths`.
- Never modify or create content under `forbidden_paths`.
- Do not import material from unrelated local repositories.
- This repository is public; commit only content suitable for public disclosure.
- Run every acceptance command and record its actual exit code.
- Stop after two consecutive tool failures.
- Write the required result file before claiming completion.
- Do not start another task automatically.
