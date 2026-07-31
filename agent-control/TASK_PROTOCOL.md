# Task Protocol

## Purpose

This protocol allows a local agent and an external reviewer to coordinate through repository files, commits, pull requests, and machine validation rather than relying on shared chat context.

## Lifecycle states

Task execution and acceptance follow distinct stages:

### Agent execution states

- **in_progress**: Active execution underway
- **interrupted**: Execution stopped before completion (e.g., context limit, tool failures)
- **cancelled**: User terminated execution before task completion
- **submitted_for_review**: Technical implementation candidate complete; awaiting review

Agent cancellation does not imply failure, technical completion, owner acceptance, or closure. Persisted repository evidence may establish candidate technical completion.

### Review and acceptance states

- **technical_completion**: Implementation candidate complete; all required artifacts present
  - **candidate_complete**: Technical work finished; validation passed
  - **changes_requested**: Reviewer identified required corrections
- **reviewer_acceptance**: External reviewer formally accepted the technical implementation
- **owner_acceptance**: Repository owner authorized formal closure or next phase
  - **pending**: Technical/reviewer acceptance achieved; awaiting owner decision
  - **accepted**: Owner explicitly authorized closure, merge, or next task
- **formal_closure**: Task permanently closed; no further changes permitted without reopening

### Critical distinctions

- Agent execution (cancelled, interrupted) ≠ technical completion
- Technical completion (candidate complete) ≠ reviewer acceptance
- Reviewer acceptance ≠ owner acceptance
- Owner acceptance ≠ formal closure (merge, archive, next-task start)

A GitHub review submitted through the owner account is reviewer evidence unless the contract explicitly records an owner authorization decision.

Only a new executable contract containing an unambiguous owner authorization may transition owner acceptance, formal closure, pull request merge, or next-task authorization.

## Required task fields

Every task must declare:

- `task_id`
- `status`
- `objective`
- `inputs`
- `allowed_paths`
- `forbidden_paths`
- `acceptance_commands`
- `completion_conditions`
- `stop_conditions`
- `result_file`

## Start procedure

1. Pull the default branch.
2. Read `AGENTS.md` and `agent-control/CURRENT_TASK.yaml`.
3. Confirm task scope without modifying files.
4. Create the task branch specified by the task file.
5. Execute only the declared task.

## Tool-failure semantics

A failed source fetch is not automatically a task-level tool failure.

Count a failure toward a stop condition only when all of the following are true:

1. the failed operation is required to complete the task;
2. the same operation has been attempted again using the declared fallback;
3. no equivalent primary-source or deterministic alternative is available;
4. continuing would require guessing, lowering the evidence standard, or leaving the task state unpersisted.

Do **not** combine unrelated failures into one consecutive-failure count. In particular:

- failures on two different websites are separate candidate failures;
- failure to fetch an English page does not block use of an accessible official page in another language;
- one inaccessible source candidate does not block research when another primary candidate can cover the same question;
- optional Issue access is not a required operation when `CURRENT_TASK.yaml` contains the executable contract.

For source research, record inaccessible candidates and continue until either the source target is met or the task-specific source-exhaustion condition is reached.

## Progress persistence

Large tasks may span more than one agent session.

If session context is ending but no stop condition is triggered:

1. persist all verified work;
2. write the result file with `status: in_progress`;
3. record the last completed stage and exact next action;
4. commit and push the task branch;
5. resume from repository state in a later session.

Context length alone is not a blocker and must not be reported as task failure.

## Completion procedure

1. Run all acceptance commands.
2. Record exit codes and unresolved issues.
3. Write the declared result JSON.
4. Commit and push the task branch.
5. Open a Draft PR.
6. Stop. Do not merge and do not begin another task.

## Result schema

```json
{
  "protocol_version": 2,
  "task_id": "",
  "status": "in_progress | completed | blocked | failed",
  "branch": "",
  "commit": "",
  "last_completed_stage": "",
  "next_action": "",
  "files_changed": [],
  "validation": [
    {
      "command": "",
      "exit_code": 0
    }
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

Use abstract examples or public sources where necessary.
