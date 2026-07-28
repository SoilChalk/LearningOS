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
  "protocol_version": 1,
  "task_id": "",
  "status": "completed | blocked | failed",
  "branch": "",
  "commit": "",
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
