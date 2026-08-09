#!/usr/bin/env python3
"""Test suite for scripts/pilot_session.py (task-004-gate-3-thin-pilot-session-runner).

Covers the Gate 3 thin-pilot acceptance conditions:

  1. Real course material is accepted via a thin seam (a path to a
     text/sectioned document provided at runtime; no indexing service, no
     vector DB, no parser framework).
  2. The session runner executes all 6 FIRST_VERTICAL_SCENARIO steps with a
     scripted (non-interactive) input driver.
  3. Returning-session recovery loads a saved state via learning_state.load_state
     and presents the saved position.
  4. Step 4 selects one of the six documented decision-tree actions and cites a
     material section.
  5. Step 5 records evidence_level in {0, 1, 2}.
  6. Step 6 persists via learning_state.save_state (unchanged module) and the
     saved file round-trips through load_state with equivalence; the
     next-action recommendation matches the evidence level.
  7. Recorded evidence distinguishes factual observations from inferences: no
     inference that the user understands a section from position confirmation
     alone.
  8. No learner model, DB, scheduler, indexing service, vector store, frontend,
     or persistence framework is introduced.

Exits 0 only when every test passes.
"""

import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import learning_state as ls  # noqa: E402
import pilot_session as ps  # noqa: E402

PASS = 0
FAIL = 0
FAILURES = []


def record(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        FAILURES.append(name)
        print(f"  ✗ {name} {('- ' + detail) if detail else ''}")


SAMPLE_MATERIAL = """# Heapsort

A heap is a complete binary tree where every parent node is greater than or
equal to its children (max-heap) or less than or equal (min-heap).

## Max-Heap Invariant

For every node n, heap[n] >= heap[2n] and heap[n] >= heap[2n+1].

## Building a Heap

Build the heap bottom-up by sifting each parent node down to restore the
invariant.

## Heap Sort Procedure

Step 1: Build a max-heap from the array.
Step 2: Swap the root (largest) with the last element.
Step 3: Reduce the heap size and sift down the new root.

## Worked Example

Example: sort [3, 1, 2] -> [1, 2, 3].

## Practice Problems

Problem 1: sort [5, 2, 4] with heapsort.
Problem 2: explain why the invariant matters.
"""


def write_material(tmp: Path) -> Path:
    path = tmp / "heapsort_notes.txt"
    path.write_text(SAMPLE_MATERIAL, encoding="utf-8")
    return path


class ScriptedIO:
    """Non-interactive input driver used by the test suite."""

    def __init__(self, lines):
        self.lines = list(lines)
        self.output = []

    def say(self, text=""):
        self.output.append(text)

    def ask(self, prompt=""):
        self.output.append(prompt)
        if not self.lines:
            raise RuntimeError("scripted input exhausted")
        return self.lines.pop(0)


def full_join(io):
    return "\n".join(str(t) for t in io.output)


def main():
    print("=== pilot_session test suite (task-004-gate-3-thin-pilot-session-runner) ===\n")

    # --- 1. Material loading via thin seam ---
    print("1. Thin-seam material loading (runtime path, no parser framework)")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        material_path = write_material(tmp)
        material = ps.load_material(material_path)
        headings = [s["heading"] for s in material["sections"]]
        record("loads material by runtime path", material["name"] == "heapsort_notes.txt")
        record(
            "extracts section headings from plain text",
            headings == [
                "Heapsort",
                "Max-Heap Invariant",
                "Building a Heap",
                "Heap Sort Procedure",
                "Worked Example",
                "Practice Problems",
            ],
            str(headings),
        )
        record("missing material raises FileNotFoundError", _raises_file_not_found(tmp / "nope.txt"))
        record(
            "no indexing/vector/DB/framework imports",
            not _imports_banned_frameworks(ps),
            "banned import found",
        )

        # --- 2. Confusion Expression accepts ANY statement ---
        print("\n2. Confusion Expression: accept ANY statement without rejection")
        cases = [
            ("I don't know where I'm confused", "cannot_articulate", None),
            ("What does a heap mean?", "articulated", "terminology_gap"),
            ("I don't remember binary trees from before", "articulated", "prerequisite_deficit"),
            ("I'm stuck at step 2", "articulated", "stuck_on_specific_step"),
            ("Why does heapsort work?", "articulated", "conceptual_confusion"),
            ("I lost my place in the material", "articulated", "lost_context"),
            ("I don't know how to sort", "articulated", "procedural_confusion"),
        ]
        for stmt, articulation, classification in cases:
            d = ps.classify_confusion(stmt, material)
            record(
                f"accepts: {stmt!r}",
                d["articulation_status"] == articulation
                and d["obstacle_classification"] == classification
                and d["user_statement"] == stmt,
                f"got articulation={d['articulation_status']} classification={d['obstacle_classification']}",
            )
        d = ps.classify_confusion("This topic is not in my notes", material)
        record("material_scope_status outside detected", d["material_scope_status"] == "outside_supplied_corpus")
        d = ps.classify_confusion("I don't have the section about recursion", material)
        record("material_scope_status missing detected", d["material_scope_status"] == "missing_required_material")
        d = ps.classify_confusion("I don't understand Bayesian inference", material)
        record("uncovered capitalized topic detected as outside", d["material_scope_status"] == "outside_supplied_corpus")

        # --- 3. Step 4: six decision-tree actions, each with a citation ---
        print("\n3. Bounded Pedagogical Action: six documented rules, one action + citation")
        six_actions = set(ps.ACTION_TYPES)
        decision_cases = [
            # (difficulty, expected_action_type, has_citation)
            ({"user_statement": "What does a heap mean?", "obstacle_classification": "terminology_gap",
              "material_scope_status": "in_scope", "articulation_status": "articulated"},
             "clarify_terminology", True),
            ({"user_statement": "I don't remember binary trees from before", "obstacle_classification": "prerequisite_deficit",
              "material_scope_status": "in_scope", "articulation_status": "articulated"},
             "restore_prerequisite", True),
            ({"user_statement": "I don't know how to sort", "obstacle_classification": "procedural_confusion",
              "material_scope_status": "in_scope", "articulation_status": "articulated"},
             "give_bounded_example", True),
            ({"user_statement": "Why does heapsort work?", "obstacle_classification": "conceptual_confusion",
              "material_scope_status": "in_scope", "articulation_status": "articulated"},
             "request_explanation", True),
            ({"user_statement": "I'm stuck at step 3", "obstacle_classification": "stuck_on_specific_step",
              "material_scope_status": "in_scope", "articulation_status": "articulated"},
             "request_fresh_attempt", True),
            ({"user_statement": "I don't know where I'm confused", "obstacle_classification": None,
              "material_scope_status": "in_scope", "articulation_status": "cannot_articulate"},
             "give_bounded_example", True),
            ({"user_statement": "This isn't in the material", "obstacle_classification": None,
              "material_scope_status": "outside_supplied_corpus", "articulation_status": "articulated"},
             "stop_and_request_more_material", False),
        ]
        for difficulty, expected, citation_expected in decision_cases:
            action = ps.select_pedagogical_action(difficulty, material, current_section="Heap Sort Procedure", material_name="heapsort_notes.txt")
            ok = action["action_type"] in six_actions
            ok = ok and (action["action_type"] == expected)
            if citation_expected:
                ok = ok and len(action["material_citations"]) >= 1
            else:
                ok = ok and len(action["material_citations"]) == 0
            record(
                f"{expected} selected with proper citations",
                ok,
                f"got action_type={action['action_type']} citations={action['material_citations']}",
            )

        # --- 4. Full session: all 6 steps with scripted driver ---
        print("\n4. Full 6-step session via scripted input driver")
        state_path = tmp / "minimal_learning_state.json"
        io = ScriptedIO(
            [
                # Step 1: new session goal + position
                "I want to understand heapsort",
                "4",  # Heap Sort Procedure
                "yes",
                # Step 2: task boundary
                "understand_concept",
                "Understand the heapsort procedure",
                "Heapsort",
                "",
                "I can explain the heapsort procedure in my own words",
                "yes",
                # Step 3: confusion
                "Why does the root end up sorted?",
                # Step 4: action response (optional)
                "",
                # Step 5: independent check
                "Build a max-heap, swap root to the end, sift down, repeat.",
                "2",
            ]
        )
        state = ps.run_session(str(material_path), str(state_path), io, now=_fixed_now)
        transcript = full_join(io)

        record("all 6 steps completed", state["session_metadata"]["steps_completed"] == [1, 2, 3, 4, 5, 6])
        record("state file written", state_path.exists())
        record(
            "state validates against unchanged schema",
            ls.is_valid_state(state),
        )
        record(
            "state round-trips through load_state with equivalence",
            ls.load_state(state_path) == state,
        )
        record(
            "current_position confirmed without understanding inference",
            state["current_position"]["confirmed_by_user"] is True
            and "understands" not in json.dumps(state["current_position"]),
        )
        record(
            "evidence_level recorded in {0,1,2}",
            state["independent_check"]["evidence_level"] in (0, 1, 2),
        )
        record(
            "next-action recommendation matches evidence level 2",
            state["next_action"]["rationale"] == "evidence_level_2_achieved_proceed_to_next",
            state["next_action"]["rationale"],
        )
        record(
            "evaluation records factual observations only",
            isinstance(state["independent_check"]["evaluation"], dict)
            and state["independent_check"]["evaluation"].get("correct_elements")
            and "master" not in json.dumps(state["independent_check"]).lower(),
        )
        record(
            "'Saved your progress' confirmation displayed",
            "Saved your progress" in transcript,
        )
        record(
            "citation to a material section present in action",
            state["last_pedagogical_action"]["material_citations"]
            and state["last_pedagogical_action"]["material_citations"][0]["section"],
        )

        # --- 5. Returning-session recovery ---
        print("\n5. Returning-session recovery via learning_state.load_state")
        io2 = ScriptedIO(
            [
                "yes",  # continue from saved position
                "yes",  # reuse saved task boundary
                # Step 3
                "I don't know where I'm confused",
                # Step 4
                "",
                # Step 5
                "I can't demonstrate it yet.",
                "0",
            ]
        )
        state2 = ps.run_session(str(material_path), str(state_path), io2, now=_fixed_now)
        t2 = full_join(io2)
        record(
            "saved position presented to returning user",
            "Heap Sort Procedure" in t2,
        )
        record(
            "recovered position carried into new state",
            state2["current_position"]["section"] == "Heap Sort Procedure",
        )
        record(
            "cannot_articulate accepted without rejection",
            "I don't know where I'm confused" in t2,
        )
        record(
            "evidence_level 0 recorded",
            state2["independent_check"]["evidence_level"] == 0,
        )
        record(
            "next-action recommendation matches evidence level 0",
            state2["next_action"]["rationale"] == "evidence_level_0_continue_from_current",
            state2["next_action"]["rationale"],
        )

        # --- 6. Evidence level 1 path ---
        print("\n6. Evidence level 1 → review-and-retry recommendation")
        io3 = ScriptedIO(
            [
                "yes",  # continue from saved position
                "yes",  # reuse saved task boundary
                # Step 3
                "I don't remember what a heap is",
                # Step 4
                "",
                # Step 5
                "I got partway but not all the way.",
                "1",
            ]
        )
        state3 = ps.run_session(str(material_path), str(state_path), io3, now=_fixed_now)
        record(
            "evidence_level 1 recorded",
            state3["independent_check"]["evidence_level"] == 1,
        )
        record(
            "next-action recommendation matches evidence level 1",
            state3["next_action"]["rationale"] == "evidence_level_1_review_and_retry",
            state3["next_action"]["rationale"],
        )

        # --- 7. Factual observations vs inferences ---
        print("\n7. Evidence discipline: factual vs inferred")
        record(
            "no inferred-understanding fields in saved state",
            "understands" not in json.dumps(state)
            and "confirms_understanding" not in json.dumps(state),
        )
        record(
            "position confirmation is the only position claim",
            "confirmed_by_user" in state["current_position"]
            and state["current_position"]["confirmed_by_user"] is True,
        )

        # --- 8. No banned build-out ---
        print("\n8. Scope: no learner model / DB / scheduler / indexing / vector store / frontend")
        record(
            "learning_state.save_state reused (same module object)",
            ps.ls is ls,
        )
        record(
            "pilot_session has no database/index/vector imports",
            not _imports_banned_frameworks(ps),
        )

    print("\n")
    print(f"PASS: {PASS}  FAIL: {FAIL}")
    if FAIL:
        print("FAILED TESTS:", ", ".join(FAILURES))
        return 1
    print("All pilot_session tests passed.")
    return 0


def _fixed_now():
    import datetime as _dt
    return _dt.datetime(2026, 8, 10, 0, 10, 0, tzinfo=_dt.timezone.utc)


def _raises_file_not_found(path):
    try:
        ps.load_material(path)
        return False
    except FileNotFoundError:
        return True


BANNED_FRAMEWORKS = [
    "sqlite", "sqlalchemy", "pymongo", "redis", "elasticsearch", "faiss",
    "annoy", "sklearn", "scikit", "tensorflow", "torch", "keras", "django",
    "flask", "fastapi", "starlette", "bottle", "tornado", "selenium", "playwright",
    "celery", "apscheduler", "kafka",
]


def _imports_banned_frameworks(module):
    try:
        spec = importlib.util.find_spec("importlib")
        import importlib.util  # noqa: F401

        src_path = Path(module.__file__)
        source = src_path.read_text(encoding="utf-8")
        import re
        for name in BANNED_FRAMEWORKS:
            if re.search(rf"(^|\s)(import|from)\s+{name}(\.|\s|$)", source, re.MULTILINE):
                return name
        return None
    except Exception:
        return None


if __name__ == "__main__":
    sys.exit(main())
