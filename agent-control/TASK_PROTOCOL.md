# Task Protocol

## Purpose

Coordinate agentic work through Issues, short-lived branches, pull requests, deterministic CI, and machine validation — without duplicating GitHub's change/review lifecycle into source control.

## Version-management model

```
Issue/problem
→ task contract where needed (execution boundary only)
→ feature/fix branch
→ meaningful commits (feat:/fix:/test:/docs:/refactor:/chore:)
→ deterministic CI + semantic reviewer (separate)
→ correction if necessary
→ READY
→ squash merge
→ delete branch
```

- `main` is trusted current product state; no direct product development on it.
- The PR is the primary change/review record. GitHub (PR number, merged_at, merge SHA, review lifecycle) is authoritative; it is **not** mirrored into `agent-control/` or `state/`.
- Post-merge lifecycle bookkeeping is **not** committed to `main`.
- No post-merge `close(task-xxx)` / protocol-reconciliation / merge-record commits, unless the files themselves have real product-semantic changes.

## Remote execution boundary

GitHub Actions are GitHub-owned asynchronous execution. The local Agent must not synchronously watch remote workflows — no `gh run watch`, no polling loops, no `sleep` + status-read cycles, no watcher daemon, scheduler, event bus, queue, or controller.

Correct pattern:

```
push / dispatch / open PR
→ record PR number / run id / head SHA
→ perform at most one non-blocking status read
→ if the remote workflow is still running, release the foreground
```

Authoritative GitHub state is re-read only on a new wake/resume/owner interaction. This applies after merge as well: PR merge is the Git lifecycle closure; do not watch or create post-merge bookkeeping.

## Task contract

`agent-control/CURRENT_TASK.yaml` is an **execution manifest** describing only the Agent execution boundary:

- `task_id`, `status`, `objective`
- `branch`
- `allowed_paths`, `forbidden_paths`
- `acceptance_commands`, `completion_conditions`, `stop_conditions`
- `result_file`

It does **not** replace the human-facing Issue or the PR description.

`state/CURRENT_STATE.yaml` records **product / learning-experiment state** (phase, product position, next product step). It does **not** mirror GitHub lifecycle.

## Lifecycle states

Keep lifecycle semantics simple and GitHub-hosted:

- **Agent execution**: `in_progress` / `interrupted` / `cancelled` / `submitted_for_review` (recorded in the result file).
- **Review**: GitHub PR review / reviewer comment is the record. Reviewer outcomes: `READY` / `CORRECTION` / `ESCALATE`.
- **Acceptance / closure**: GitHub merge + PR metadata is the authoritative closure record. Owner acceptance is only needed at genuine human boundaries (product/security/architecture/scope).

### Critical distinctions

- Agent execution (cancelled, interrupted) ≠ technical completion.
- Technical completion ≠ reviewer acceptance.
- Reviewer acceptance ≠ owner acceptance.
- Owner acceptance ≠ formal closure (merge / next phase).

## Authorization

- Within the **Gate-scoped standing delegation**, do not re-request owner authorization for every task/merge.
- **ESCALATE** (owner decision required) only on:
  - Gate scope change or architecture decision;
  - destructive operation;
  - new/expanded permissions or secrets;
  - security-sensitive / protected-file change;
  - material new cost or new infrastructure;
  - conflicting authoritative requirements;
  - a product decision that cannot be resolved safely;
  - declaring a Gate complete and moving to the next Gate.

## Start procedure

1. Pull `main`.
2. Read `AGENTS.md` and `agent-control/CURRENT_TASK.yaml`.
3. Confirm task scope without modifying files.
4. Create the branch named in the contract (or a short-lived `feat/`/`fix/`/`chore/` branch).
5. Execute only the declared task.

## Tool-failure semantics

A failed source fetch is not automatically a task-level tool failure. Count a failure toward a stop condition only when all of the following are true:

1. the failed operation is required to complete the task;
2. the same operation has been retried using the declared fallback;
3. no equivalent primary-source or deterministic alternative is available;
4. continuing would require guessing, lowering the evidence standard, or leaving the task state unpersisted.

Do **not** combine unrelated failures into one consecutive-failure count.

## Progress persistence

Large tasks may span sessions. If context is ending with no stop condition triggered:

1. persist verified work;
2. write the result file with `status: in_progress`;
3. record the last completed stage and exact next action;
4. commit and push the task branch (or update the PR branch);
5. resume from repository state later.

## Completion procedure

1. Run all acceptance commands (deterministic CI does this too).
2. Record exit codes and unresolved issues in the result file.
3. Open (or update) a PR with a concise description (Why / What / Scope / Validation / Evidence / Risks).
4. Do not merge; the reviewer (or owner at genuine boundaries) decides.

## Result schema

```json
{
  "protocol_version": 20,
  "task_id": "",
  "status": "in_progress | submitted_for_review | completed",
  "branch": "",
  "commit": "",
  "last_completed_stage": "",
  "next_action": "",
  "files_changed": [],
  "validation": [
    { "command": "", "exit_code": 0 }
  ],
  "unresolved_issues": [],
  "claims_requiring_review": []
}
```

## Privacy and repository boundary

This is a public repository. Do not commit:

- course materials or copyrighted source files;
- personal records or mental-health notes;
- contents copied from unrelated local repositories;
- `.env` files, API keys, credentials, tokens, private URLs, or secrets;
- absolute local paths unless explicitly required and safe to disclose.
