#!/usr/bin/env python3
"""Test suite for scripts/learning_state.py (task-003-gate-3-state-persistence).

Covers the Gate 3 first-slice acceptance conditions:

  1. A valid complete state instance can be saved and reloaded with round-trip
     equivalence.
  2. Missing required field is rejected.
  3. Unknown/additional field is rejected.
  4. evidence_level outside [0, 1, 2] is rejected.
  5. Malformed state fails explicitly (no silent repair).
  6. Cross-object constraints from the schema (stop_action + in_scope + empty
     citations + stop_reason) are enforced by the same validator.

Exits 0 only when every test passes.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import learning_state as ls  # noqa: E402

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


def valid_state(**overrides):
    """Return a complete, schema-valid minimal learning-state instance."""
    state = {
        "schema_version": "1.0",
        "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
        "session_id": "session-2026-08-05T10:00:00Z",
        "created_at": "2026-08-05T10:00:00+08:00",
        "updated_at": "2026-08-05T10:05:00+08:00",
        "current_position": {
            "material_file": "course.pdf",
            "section": "Chapter 3",
            "page": "12",
            "problem_number": None,
            "confirmed_by_user": True,
            "confirmed_at": "2026-08-05T10:01:00+08:00",
        },
        "task_boundary": {
            "task_type": "understand_concept",
            "scope_description": "Understand heap data structure",
            "start_section": "Chapter 3",
            "end_section": None,
            "completion_criterion": "Explain heap operations independently",
        },
        "observed_difficulty": {
            "user_statement": "I don't know what's confusing",
            "obstacle_classification": None,
            "material_scope_status": "in_scope",
            "articulation_status": "cannot_articulate",
            "material_context": {"section": "Chapter 3", "page": "12", "problem": None},
            "expressed_at": "2026-08-05T10:03:00+08:00",
        },
        "last_pedagogical_action": {
            "action_type": "request_explanation",
            "action_details": {"explanation_requested": "Explain heapify"},
            "material_citations": [
                {"file": "course.pdf", "section": "Chapter 3", "page": "12"}
            ],
            "delivered_at": "2026-08-05T10:04:00+08:00",
            "user_response": None,
            "escalation_count": 0,
        },
        "independent_check": {
            "requested": False,
            "check_type": None,
            "user_response": None,
            "evidence_level": 0,
            "evaluation": None,
            "checked_at": None,
        },
        "next_action": {
            "recommendation": "Continue from current position",
            "rationale": "evidence_level_0_continue_from_current",
            "suggested_material_section": "Chapter 3",
        },
        "session_metadata": {
            "duration_seconds": 300,
            "position_recovery_seconds": 60,
            "steps_completed": [1, 2, 3, 4, 5, 6],
        },
    }
    state.update(overrides)
    return state


def main():
    print("=== learning_state test suite (task-003-gate-3-state-persistence) ===\n")

    # --- Test 1: baseline valid instance ---
    print("1. Valid complete instance validates")
    base = valid_state()
    record("valid instance passes validate_state", ls.is_valid_state(base))

    # --- Test 2: round-trip save/load equivalence ---
    print("2. Save/load round-trip equivalence")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "minimal_learning_state.json"
        ls.save_state(base, path)
        loaded = ls.load_state(path)
        record("saved file exists and is valid JSON", path.exists())
        record("reloaded instance equals original", loaded == base)
        raw = json.loads(path.read_text(encoding="utf-8"))
        record("written file is parseable JSON object", isinstance(raw, dict))
        record(
            "evidence_level 0 round-trips unchanged",
            loaded["independent_check"]["evidence_level"] == 0,
        )

    # --- Test 3: missing required field is rejected ---
    print("3. Missing required fields rejected")
    for missing in (
        "schema_version",
        "scenario_id",
        "session_id",
        "created_at",
        "updated_at",
        "current_position",
        "task_boundary",
        "observed_difficulty",
        "last_pedagogical_action",
        "independent_check",
        "next_action",
    ):
        broken = valid_state()
        del broken[missing]
        record(f"missing {missing} rejected", not ls.is_valid_state(broken))

    # Nested required fields
    broken_nested = valid_state()
    del broken_nested["current_position"]["material_file"]
    record("nested missing current_position.material_file rejected", not ls.is_valid_state(broken_nested))
    broken_nested = valid_state()
    del broken_nested["independent_check"]["requested"]
    record("nested missing independent_check.requested rejected", not ls.is_valid_state(broken_nested))

    # --- Test 4: unknown/additional field is rejected ---
    print("4. Unknown/additional fields rejected")
    extra_top = valid_state()
    extra_top["learner_profile"] = {"level": "beginner"}
    record("top-level unknown field rejected", not ls.is_valid_state(extra_top))
    extra_nested = valid_state()
    extra_nested["current_position"]["favorite_color"] = "blue"
    record("nested unknown field rejected", not ls.is_valid_state(extra_nested))

    # --- Test 5: evidence_level outside [0,1,2] rejected ---
    print("5. evidence_level outside [0,1,2] rejected")
    for bad_value in (3, -1, 4, 1.5, "2"):
        broken = valid_state()
        broken["independent_check"]["evidence_level"] = bad_value
        record(f"evidence_level {bad_value!r} rejected", not ls.is_valid_state(broken))
    for good_value in (0, 1, 2):
        good = valid_state()
        good["independent_check"]["evidence_level"] = good_value
        record(f"evidence_level {good_value} accepted", ls.is_valid_state(good))

    # --- Test 6: malformed state fails explicitly (no silent repair) ---
    print("6. Malformed state fails explicitly")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"

        # Non-dict instance
        record("validate_state(list) returns errors", bool(ls.validate_state([1, 2, 3])))
        record("validate_state(str) returns errors", bool(ls.validate_state("not-a-state")))

        # save_state must not create a file for invalid state
        try:
            ls.save_state([], path)
            record("save_state(list) raises LearningStateError", False)
        except ls.LearningStateError:
            record("save_state(list) raises LearningStateError", True)
        record("no file written for invalid state", not path.exists())

        # Malformed JSON file
        path.write_text("{not valid json", encoding="utf-8")
        try:
            ls.load_state(path)
            record("load_state(malformed JSON) raises LearningStateError", False)
        except ls.LearningStateError as exc:
            record("load_state(malformed JSON) raises LearningStateError", "malformed" in str(exc).lower())

        # Valid JSON but not an object
        path.write_text('"just a string"', encoding="utf-8")
        try:
            ls.load_state(path)
            record("load_state(non-object JSON) raises LearningStateError", False)
        except ls.LearningStateError:
            record("load_state(non-object JSON) raises LearningStateError", True)

        # Valid JSON, schema-valid object but invalid per schema
        invalid = valid_state()
        invalid["independent_check"]["evidence_level"] = 7
        path.write_text(json.dumps(invalid), encoding="utf-8")
        try:
            ls.load_state(path)
            record("load_state(schema-invalid) raises LearningStateError", False)
        except ls.LearningStateError:
            record("load_state(schema-invalid) raises LearningStateError", True)

        # Missing file
        try:
            ls.load_state(Path(tmp) / "does-not-exist.json")
            record("load_state(missing file) raises LearningStateError", False)
        except ls.LearningStateError:
            record("load_state(missing file) raises LearningStateError", True)

    # --- Test 7: cross-object stop-action constraint (schema allOf) ---
    print("7. Cross-object constraints enforced")
    stop_in_scope = valid_state(
        **{
            "last_pedagogical_action": {
                "action_type": "stop_and_request_more_material",
                "action_details": {"stop_reason": "Need more examples"},
                "material_citations": [],
                "delivered_at": "2026-08-05T10:04:00+08:00",
            },
            "observed_difficulty": {
                "user_statement": "Don't understand pivot selection",
                "obstacle_classification": "procedural_confusion",
                "material_scope_status": "in_scope",
                "articulation_status": "articulated",
                "expressed_at": "2026-08-05T10:03:00+08:00",
            },
        }
    )
    record(
        "stop_action + in_scope + empty citations rejected",
        not ls.is_valid_state(stop_in_scope),
    )

    stop_missing_material = valid_state(
        **{
            "last_pedagogical_action": {
                "action_type": "stop_and_request_more_material",
                "action_details": {"stop_reason": "Memoization not covered"},
                "material_citations": [],
                "delivered_at": "2026-08-05T10:04:00+08:00",
            },
            "observed_difficulty": {
                "user_statement": "Material doesn't cover memoization",
                "obstacle_classification": "prerequisite_deficit",
                "material_scope_status": "missing_required_material",
                "articulation_status": "articulated",
                "expressed_at": "2026-08-05T10:03:00+08:00",
            },
            "next_action": {
                "recommendation": "Request memoization material",
                "rationale": "escalation_threshold_review_offline",
            },
        }
    )
    record(
        "stop_action + missing_required_material + empty citations + stop_reason accepted",
        ls.is_valid_state(stop_missing_material),
    )

    # --- Test 8: save rejects schema-invalid state without touching existing file ---
    print("8. save_state leaves existing file untouched on invalid state")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"
        ls.save_state(valid_state(), path)
        before = path.read_bytes()
        broken = valid_state()
        broken["extra_field"] = True
        try:
            ls.save_state(broken, path)
            record("save_state(invalid) raises LearningStateError", False)
        except ls.LearningStateError:
            record("save_state(invalid) raises LearningStateError", True)
        record("existing file bytes unchanged", path.read_bytes() == before)

    print()
    print(f"Tests passed: {PASS}, failed: {FAIL}")
    if FAIL:
        print("Failed tests:")
        for name in FAILURES:
            print(f"  - {name}")
        return 1
    print("✓ All learning_state tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
