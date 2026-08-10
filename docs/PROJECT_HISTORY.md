# Project History

> **Retrospective project history reconstructed from existing repository records.**
>
> This document was written after the fact from the repository's actual Git history, Issues, and Pull Requests. It does not fabricate processes, dates, releases, or approvals that are not present in the records. Where a stage was driven by an internal agent workflow rather than a human-readable issue, that is stated explicitly.

## Milestones

### 1. Core research + local agent protocol (Gate 1)

- **Issue**: [#1 — 建立 Learning OS 核心调研与本地 Agent 交接协议](https://github.com/SoilChalk/LearningOS/issues/1) (2026-07-28)
- **PR**: [#2 — Establish core research workflow](https://github.com/SoilChalk/LearningOS/pull/2) (merged 2026-07-28)
- **What happened**: Core product research (8 verified sources), the first vertical scenario direction, and a local agent handoff protocol (`AGENTS.md`, `agent-control/`, `state/`) were established. The research phase concluded **with documented limitations** — not a claim that all design questions were answered.
- **Evidence**: `sources/source-ledger.json` (8 sources), `docs/RESEARCH_QUESTIONS.md`, `docs/REFERENCE_SYSTEM_MATRIX.md`, `docs/DESIGN_GATES.md`.

### 2. First vertical scenario design (Gate 2)

- **PR**: [#3 — Task 002: First Vertical Scenario Design](https://github.com/SoilChalk/LearningOS/pull/3) (merged 2026-08-02)
- **What happened**: The first vertical scenario ("Source-Grounded Learning Recovery and Independent Completion Check") was specified with entry/exit criteria, a 6-step flow, a pedagogical action decision tree, and a minimal learning-state schema.
- **Evidence**: `docs/FIRST_VERTICAL_SCENARIO.md`, `docs/PEDAGOGICAL_ACTION_DECISION_TREE.md`, `templates/MINIMAL_LEARNING_STATE.schema.json`. Gate 2 was formally closed (commit `5daf7a5`).

### 3. Agent workflow experimentation

- **What happened**: Before building product features, the project experimentally validated an automated `executor → PR → reviewer → correction → READY` loop using [GitHub Agentic Workflows (gh-aw)](https://github.com/github/gh-aw) with a DeepSeek model via the Copilot BYOK path. This work happened in a **separate disposable repository** (`SoilChalk/learningos-agent-loop-spike`) and was intentionally not part of LearningOS history.
- **Why it matters**: It de-risked the orchestration approach used in the next milestones. The LearningOS repository itself contains only the adapted workflows (see below).

### 4. gh-aw integration on LearningOS

- **PR**: [#5 — infra: gh-aw executor + reviewer workflows (DeepSeek V4 Flash)](https://github.com/SoilChalk/LearningOS/pull/5) (merged 2026-08-09)
- **What happened**: `executor` and `reviewer` agentic workflows were added under `.github/workflows/`, contract-aware (they read `agent-control/CURRENT_TASK.yaml`). A dispatch-based loop (no personal access token) was used; the reviewer was made triggerable by the Actions bot via an `on.bots` allowlist.
- **Note**: This was infrastructure, not a product feature.

### 5. Learning-state persistence (Gate 3, slice 1)

- **PR**: [#7 — task-003-gate-3-state-persistence](https://github.com/SoilChalk/LearningOS/pull/7) (merged 2026-08-09)
- **What happened**: `scripts/learning_state.py` — validate/save/load a minimal learning state against the existing schema, with **atomic writes** (same-directory temp file + `os.replace()`) so a failed write never corrupts an existing state. A deterministic test covers the write-phase failure case.
- **Evidence**: `scripts/learning_state.py`, `scripts/test_learning_state.py`, `agent-control/results/task-003.json`.

### 6. Thin real-session runner (Gate 3, slice 2)

- **PR**: [#9 — task-004-gate-3-thin-pilot-session-runner](https://github.com/SoilChalk/LearningOS/pull/9) (merged 2026-08-09)
- **What happened**: `scripts/pilot_session.py` — a thin interactive runner for the 6-step scenario flow, reusing `learning_state.py` unchanged. This is the seam that makes a first real-material pilot runnable.
- **Evidence**: `scripts/pilot_session.py`, `scripts/test_pilot_session.py`, `agent-control/results/task-004.json`.

### 7. Current direction: VS Code interaction surface

- **What happened**: The product direction was narrowed to **personal learning execution / friction-reduction layer**, with **VS Code chat** as the intended interaction surface. The goal is a first real-material learning pilot where the owner participates as the learner.
- **Status**: Not yet run; this is the current open question.

### 8. Repository hygiene baseline

- **Issue**: [#10 — Repo hygiene baseline](https://github.com/SoilChalk/LearningOS/issues/10)
- **What happened**: This document, the public README, the development convention, a PR template, and deterministic CI were added so the repository presents a clear, credible trajectory. No history was rewritten and no releases were created retroactively.

## Commit prefix convention

Recent commits use lightweight semantic prefixes (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`). Earlier commits used task/protocol-style messages (`task-003:`, `Protocol 20:`, etc.). See `docs/DEVELOPMENT.md`.

## Known open items (from real records)

- No LICENSE is selected (owner decision pending).
- No releases/tags exist yet; a `v0.1.0-alpha` prerelease is proposed only after the first real VS Code learning interaction + real-material pilot.
- The `README → merge → lifecycle closure` loop is not yet fully event-driven (see `docs/DEVELOPMENT.md`).
