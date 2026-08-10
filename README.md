# LearningOS

**Personal learning execution / friction-reduction layer.**

LearningOS is a personal project focused on the operations *around* learning: starting, resuming position, deciding the next step, recovering from being stuck, moving from explanation to independent completion, and continuing across sessions. It is not a course catalog, a knowledge graph, or a full learner-modeling platform.

The core idea: **don't make the learner operate the system — make the system operate around the learner.** The intended interaction surface is a VS Code chat session where the learner expresses a real learning intent and the system minimizes every operational step between that intent and an actual learning action.

## Why this focus

Most friction in self-directed learning is not "understanding the material" — it is operational overhead:

- **Starting**: figuring out what to work on today.
- **Resuming**: remembering where you left off.
- **Deciding the next step**: choosing the smallest useful next action.
- **Recovering from stuck**: translating "I don't know where I'm confused" into a concrete move.
- **Independent completion**: verifying that an explanation actually became usable knowledge.
- **Continuation**: not having to re-read a long chat history next session.

LearningOS is designed to reduce exactly these costs, in one learning flow at a time.

## Current real capabilities

The repository currently contains a thin vertical slice of the intended experience:

- **Learning-state persistence** (`scripts/learning_state.py`): validate, save, and load a minimal learning state (position, task boundary, confusion, evidence level, next action) against a JSON Schema. Writes are atomic (same-directory temp file + `os.replace()`), so a failed write never corrupts an existing state.
- **Thin session runner** (`scripts/pilot_session.py`): a minimal interactive 6-step flow for one real-material session — position recovery, task boundary, natural-language confusion expression, one source-grounded pedagogical action, an independent completion check, and state persistence.
- **Authoritative validation scripts** for the internal research/design records (Gate 1 / Gate 2), kept green by deterministic CI.

These are deliberately thin: no learner model, no database, no scheduler, no indexing service, no frontend.

## Architecture / components

```
learner ──▶ VS Code chat (target interaction surface)
               │
               ▼
        pilot_session.py        # thin 6-step session flow
               │
               ▼
        learning_state.py       # validate / save / load minimal state (atomic)
               │
               ▼
   MINIMAL_LEARNING_STATE.schema.json
```

Supporting structure:

- `docs/` — research questions, design gates, the first vertical scenario, pedagogical action decision tree, and this project's history.
- `templates/` — JSON Schemas used by validation.
- `sources/` — verified source ledger for the research phase.
- `state/`, `agent-control/` — internal control-plane files used by the agent workflows (see Development / Internal below).

## Quick start

```bash
# Validate and save/load a minimal learning state
python3 -c "import sys; sys.path.insert(0,'scripts'); import learning_state"
python3 scripts/test_learning_state.py

# Run the thin session runner against a real text material file
python3 scripts/pilot_session.py --material path/to/course-material.txt
```

## Tests

Deterministic acceptance suite (no LLM involved):

```bash
for f in scripts/*.py; do python3 -m py_compile "$f"; done
python3 scripts/test_learning_state.py
python3 scripts/test_pilot_session.py
python3 scripts/validate_task_002.py
python3 scripts/validate_source_records.py
bash scripts/test_task_002_negative.sh
bash scripts/test_validation_negative.sh
bash scripts/test_control_state.sh
```

These are run automatically by the GitHub Actions workflow in `.github/workflows/ci.yml`.

## Current maturity / limitations

- **Experimental**: this is an early personal project, not a product.
- The session runner is a thin seam; material indexing and richer pedagogy are intentionally not built yet.
- No learner model, no automatic mastery classification, no multi-course support.
- No claims are made that the "LearningOS architecture" is validated — only individual slices have been exercised.

## Development status

- First vertical scenario designed (Gate 2) and research phase completed with documented limitations (Gate 1).
- Gate 3 (minimum viable pilot) is in progress; the goal is one real-material learning session with the owner as learner.
- Current next step: run the first real-material pilot in a VS Code chat session.

See `docs/PROJECT_HISTORY.md` for an honest, evidence-linked retrospective, and `docs/DEVELOPMENT.md` for the default contribution workflow.

## Privacy boundary

This repository must never contain: course materials, personal learning records, local checkpoints, API keys, `.env` files, secrets, tokens, private URLs, or absolute sensitive local paths. Learning content used at runtime stays on the learner's machine.

## Development / Internal

The internal control plane used by the agentic workflows (`agent-control/`, `state/`, `AGENTS.md`, `.github/workflows/`) is documented separately in `docs/DEVELOPMENT.md` and `docs/PROJECT_HISTORY.md`. It is not part of the public-facing product story above.
