#!/usr/bin/env python3
"""Validate the active task contract, current state, and declared result record."""

import argparse
import json
import sys
from pathlib import Path


LIFECYCLE_FIELDS = (
    "previous_agent_execution",
    "technical_completion",
    "reviewer_acceptance",
    "latest_reviewer_record",
    "owner_acceptance",
    "lifecycle_status",
    "formal_closure",
    "task_002_status",
)


def parse_scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "yes"}:
        return True
    if lowered in {"false", "no"}:
        return False
    if value.isdigit():
        return int(value)
    return value


def parse_yaml_simple(content: str):
    """Parse the mapping/scalar subset used by control files."""
    root = {}
    stack = [(-1, root)]

    for raw_line in content.splitlines():
        stripped = raw_line.lstrip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        if ":" not in stripped:
            continue

        indent = len(raw_line) - len(stripped)
        key, _, raw_value = stripped.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]

        if raw_value:
            current[key] = parse_scalar(raw_value)
        else:
            child = {}
            current[key] = child
            stack.append((indent, child))

    return root


def read_yaml(path: Path):
    try:
        return parse_yaml_simple(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read YAML {path}: {exc}", file=sys.stderr)
        return None


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read JSON {path}: {exc}", file=sys.stderr)
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-task")
    parser.add_argument("--current-state")
    parser.add_argument("--task-result")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    task_path = Path(args.current_task) if args.current_task else repo_root / "agent-control" / "CURRENT_TASK.yaml"
    state_path = Path(args.current_state) if args.current_state else repo_root / "state" / "CURRENT_STATE.yaml"

    task = read_yaml(task_path)
    state = read_yaml(state_path)
    if not task or not state:
        return 1

    if args.task_result:
        result_path = Path(args.task_result)
    else:
        declared = task.get("result_file")
        if not isinstance(declared, str) or not declared:
            print("ERROR: CURRENT_TASK.yaml must declare result_file", file=sys.stderr)
            return 1
        result_path = repo_root / declared

    result = read_json(result_path)
    if not result:
        return 1

    errors = []
    task_id = task.get("task_id")
    state_id = state.get("task_id")
    result_id = result.get("task_id")
    if not (task_id == state_id == result_id):
        errors.append(f"task_id mismatch: contract={task_id!r}, state={state_id!r}, result={result_id!r}")

    task_status = task.get("status")
    state_status = state.get("status")
    result_status = result.get("status")
    if not (task_status == state_status == result_status):
        errors.append(
            f"status mismatch: contract={task_status!r}, state={state_status!r}, result={result_status!r}"
        )

    task_lifecycle = task.get("lifecycle") or task.get("truth_to_preserve") or {}
    state_lifecycle = state.get("lifecycle") or {}
    result_lifecycle = result.get("lifecycle") or {}

    for field in LIFECYCLE_FIELDS:
        values = (
            task_lifecycle.get(field),
            state_lifecycle.get(field),
            result_lifecycle.get(field),
        )
        if any(value is None for value in values):
            errors.append(f"missing lifecycle field {field}: {values!r}")
        elif not (values[0] == values[1] == values[2]):
            errors.append(
                f"lifecycle mismatch for {field}: contract={values[0]!r}, state={values[1]!r}, result={values[2]!r}"
            )

    formal_closure = task_lifecycle.get("formal_closure")
    owner_acceptance = task_lifecycle.get("owner_acceptance")
    lifecycle_status = task_lifecycle.get("lifecycle_status")

    if formal_closure is True:
        if owner_acceptance != "accepted":
            errors.append("formal closure requires owner_acceptance=accepted")
        if lifecycle_status not in {"formally_closed", "closed"}:
            errors.append("formal closure requires a closed lifecycle_status")
    elif task_status == "ready":
        if lifecycle_status != "ready":
            errors.append("a ready contract requires lifecycle_status=ready")
        if task_lifecycle.get("technical_completion") != "not_started":
            errors.append("a newly ready task requires technical_completion=not_started")

    if errors:
        print("Control state consistency check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"✓ Control state consistency check passed for {task_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
