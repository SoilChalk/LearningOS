#!/usr/bin/env python3
"""
Control State Consistency Checker

Validates that lifecycle claims in CURRENT_TASK.yaml, CURRENT_STATE.yaml,
and task-001.json agree on required semantic values and that forbidden
transitions are absent.

Uses only Python standard library. Returns 0 only when all required
consistency conditions are met.
"""

import json
import re
import sys
from pathlib import Path


def parse_yaml_simple(content):
    """
    Simple YAML parser for the limited subset used in this repository.
    Handles only the required fields without external dependencies.
    """
    data = {}
    lines = content.split('\n')
    i = 0
    stack = [data]
    indent_stack = [-1]

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            i += 1
            continue

        # Calculate indentation
        indent = len(line) - len(stripped)

        # Pop stack if dedenting
        while indent_stack and indent < indent_stack[-1]:
            stack.pop()
            indent_stack.pop()

        # Parse key-value or section
        if ':' in stripped:
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            current = stack[-1]

            if value:
                # Inline value
                # Handle quoted strings
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                # Handle booleans
                elif value.lower() in ('true', 'yes'):
                    value = True
                elif value.lower() in ('false', 'no'):
                    value = False
                # Handle numbers
                elif value.isdigit():
                    value = int(value)

                current[key] = value
            else:
                # New section
                current[key] = {}
                stack.append(current[key])
                indent_stack.append(indent)

        i += 1

    return data


def read_yaml_file(filepath):
    """Read and parse a YAML file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return parse_yaml_simple(content)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Failed to parse {filepath}: {e}", file=sys.stderr)
        return None


def read_json_file(filepath):
    """Read and parse a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}", file=sys.stderr)
        return None


def get_nested(data, *keys, default=None):
    """Safely access nested dictionary keys."""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def main():
    repo_root = Path(__file__).parent.parent

    # Read all three files
    current_task = read_yaml_file(repo_root / 'agent-control' / 'CURRENT_TASK.yaml')
    current_state = read_yaml_file(repo_root / 'state' / 'CURRENT_STATE.yaml')
    task_result = read_json_file(repo_root / 'agent-control' / 'results' / 'task-001.json')

    if not all([current_task, current_state, task_result]):
        print("ERROR: Cannot read required files", file=sys.stderr)
        return 1

    errors = []

    # Check task_id consistency
    task_task_id = current_task.get('task_id', '')
    state_task_id = current_state.get('task_id', '')
    result_task_id = task_result.get('task_id', '')

    # For control-plane-repair task, the subject is task-001-core-research
    if task_task_id == 'task-001-control-plane-repair':
        expected_subject = get_nested(current_task, 'truth_to_preserve', 'subject_task_id')
        if expected_subject != state_task_id:
            errors.append(f"State task_id '{state_task_id}' does not match control repair subject '{expected_subject}'")
        if expected_subject != result_task_id:
            errors.append(f"Result task_id '{result_task_id}' does not match control repair subject '{expected_subject}'")
    elif task_task_id == state_task_id == result_task_id:
        # Normal case: all match
        pass
    else:
        errors.append(f"Task IDs disagree: task={task_task_id}, state={state_task_id}, result={result_task_id}")

    # Check for forbidden stale status
    task_status = current_task.get('status', '')
    if task_status == 'changes_requested':
        # This is only allowed if we're in a control-plane-repair that's explicitly fixing it
        if task_task_id != 'task-001-control-plane-repair':
            errors.append(f"Stale 'changes_requested' status in CURRENT_TASK.yaml")

    # Check lifecycle consistency
    # Extract lifecycle from each source
    task_lifecycle = current_task.get('truth_to_preserve', {})
    state_lifecycle = current_state.get('lifecycle', {})
    result_lifecycle = task_result.get('lifecycle', {})

    # Required semantic values
    required_checks = [
        ('owner_acceptance', 'pending'),
        ('formal_closure', False),
        ('task_002_status', 'not_started'),
    ]

    for field, expected in required_checks:
        task_val = task_lifecycle.get(field)
        state_val = state_lifecycle.get(field)
        result_val = result_lifecycle.get(field)

        # All three should agree
        if task_val != expected:
            errors.append(f"CURRENT_TASK truth_to_preserve.{field} is '{task_val}', expected '{expected}'")
        if state_val != expected:
            errors.append(f"CURRENT_STATE lifecycle.{field} is '{state_val}', expected '{expected}'")
        if result_val != expected:
            errors.append(f"task-001.json lifecycle.{field} is '{result_val}', expected '{expected}'")

    # Check for forbidden transitions
    if task_lifecycle.get('owner_acceptance') == 'accepted':
        # Only allowed if explicitly authorized in the contract
        auth = current_task.get('owner_authorization', {})
        if 'formally_close_task_001' not in auth.get('authorized', []):
            errors.append("owner_acceptance marked 'accepted' without explicit authorization")

    if task_lifecycle.get('formal_closure') is True:
        errors.append("formal_closure marked True without authorization")

    if task_lifecycle.get('task_002_status') != 'not_started':
        errors.append(f"Task 002 status is '{task_lifecycle.get('task_002_status')}', should be 'not_started'")

    # Report results
    if errors:
        print("Control state consistency check FAILED:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("✓ Control state consistency check passed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
