# LearningOS

This repository is the public, non-sensitive control surface for the Learning OS project.

## Current authority

Local agents must read, in order:

1. `AGENTS.md`
2. `agent-control/TASK_PROTOCOL.md`
3. `agent-control/CURRENT_TASK.yaml`

The executable task contract lives in `agent-control/CURRENT_TASK.yaml`. GitHub Issue #1 provides discussion context, but Issue access is optional when the executable contract is present in the repository.

## Current task

`task-001-core-research`

The task is staged and resumable. Source retrieval failures are scoped per required operation and per source candidate. Unrelated website failures must not be combined into a global stop condition. See the task protocol and current task contract for the exact fallback and stop rules.

## Privacy boundary

Do not commit course materials, personal records, local checkpoints, API keys, `.env` files, secrets, tokens, private URLs, absolute sensitive local paths, or unrelated contents from other local repositories.
