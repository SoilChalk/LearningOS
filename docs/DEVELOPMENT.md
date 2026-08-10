# Development

Short default workflow for this repository. Human-readable Issue for *why / outcome*; machine execution scope lives in the task contract.

## Default workflow

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

- **Human-facing Issue** explains why and the intended outcome.
- **`agent-control/CURRENT_TASK.yaml`** is the machine execution manifest (scope, acceptance commands, stop conditions). It does **not** replace human-readable history or the PR.
- **`state/CURRENT_STATE.yaml`** records product / learning-experiment state, not GitHub lifecycle.
- **Branch naming**: existing `agent/task-*` branches are relied on by the automation and stay as-is; new work uses short-lived `feat/`/`fix/`/`chore/` branches.

## Commit messages

Lightweight semantic prefixes (no commitlint):

- `feat:` — new capability
- `fix:` — bug fix
- `test:` — tests
- `docs:` — documentation
- `refactor:` — behavior-preserving change
- `chore:` — maintenance / tooling

Example: `fix(learning_state): atomic save via same-dir temp + os.replace`.

## Deterministic CI

`.github/workflows/ci.yml` runs the authoritative, stable Python/shell acceptance tests. It never calls an LLM and does not replicate the gh-aw orchestration.

## Local Git configuration (recommended)

Set once per local clone (do not touch global config):

```bash
git config --local pull.ff only
git config --local fetch.prune true
git config --local rerere.enabled true
git config --local rebase.autoStash true
```

## Main-history rule

- PR branch keeps implementation/test/reviewer-correction commits.
- `main` defaults to **squash merge** producing one semantically clear product commit, e.g. `feat(vscode): add native LearningOS learning entry (#12)`.
- Do **not** generate separate `close(task-xxx)`, lifecycle-sync, protocol-reconciliation, or merge-record bookkeeping commits on `main` — unless those files have real product-semantic changes.

## Control-plane note

The `READY → merge → lifecycle closure` loop currently depends on a foreground local agent (`gh run watch` + manual merge). This is a known gap; prefer GitHub-native auto-merge + a reviewer-required check run if a new implementation task needs it. Per the Remote execution boundary rule, local agents never poll/wait on remote GitHub Actions.
