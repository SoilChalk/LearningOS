# Task Protocol

## Purpose

This protocol allows a local agent and an external reviewer to coordinate through repository files, commits, pull requests, and machine validation rather than relying on shared chat context.

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
