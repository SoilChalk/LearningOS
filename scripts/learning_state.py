#!/usr/bin/env python3
"""Minimal learning-state persistence for the First Vertical Scenario (Step 6).

Implements the save/load/validation slice required by Gate 3 first task A:

  (a) save_state   - validate a learning-state instance against the schema and
                     persist it as JSON
  (b) load_state   - read a state file, parse it, validate it, and return the
                     instance
  (c) validate_state / is_valid_state - validate an instance against
                     templates/MINIMAL_LEARNING_STATE.schema.json (JSON Schema
                     Draft-07; 11 required top-level fields; additionalProperties
                     false; evidence_level enum 0|1|2).

Design constraints (owner authorization, task-003-gate-3-state-persistence):

  * Reuses the existing schema and the existing validation infrastructure
    (jsonschema.Draft7Validator, the same engine used by scripts/validate_task_002.py
    and scripts/test_task_002_negative.sh). The schema is never modified.
  * No learner model, no database, no scheduler, no new persistence abstraction.
  * save_state writes atomically: content is written to a temporary file in the
    same directory as the target and os.replace()d over it only after the
    temporary file is fully written and closed. An existing state file is
    therefore never truncated or left partially written by a write-phase
    failure; on any failure the temporary file is removed.
  * Malformed or invalid state fails explicitly (LearningStateError); there is
    no silent repair, coercion, or partial write.
"""

import json
import os
import tempfile
from pathlib import Path


class LearningStateError(ValueError):
    """Raised when a learning-state instance cannot be validated, saved, or loaded."""


SCHEMA_RELATIVE_PATH = Path("templates") / "MINIMAL_LEARNING_STATE.schema.json"


def _repo_root() -> Path:
    """Absolute path of the repository root (parent of this scripts/ directory)."""
    return Path(__file__).resolve().parent.parent


def default_schema_path() -> Path:
    """Absolute path of the minimal learning-state JSON schema."""
    return _repo_root() / SCHEMA_RELATIVE_PATH


def load_schema(schema_path=None) -> dict:
    """Load the state JSON Schema as a dict.

    Args:
        schema_path: Optional path to a schema file. Defaults to the repository
            schema templates/MINIMAL_LEARNING_STATE.schema.json.
    """
    path = Path(schema_path) if schema_path is not None else default_schema_path()
    try:
        with open(path, encoding="utf-8") as f:
            schema = json.load(f)
    except OSError as exc:
        raise LearningStateError(f"cannot read schema file {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise LearningStateError(f"schema file {path} is not valid JSON: {exc}") from exc
    if not isinstance(schema, dict):
        raise LearningStateError(f"schema file {path} must contain a JSON object")
    return schema


def _make_validator(schema: dict):
    """Build a JSON Schema Draft-07 validator using the existing jsonschema dependency."""
    try:
        from jsonschema import Draft7Validator
    except ImportError as exc:  # pragma: no cover - environment dependency check
        raise LearningStateError(
            "jsonschema is required for state validation; install it with "
            "'python3 -m pip install jsonschema'"
        ) from exc
    return Draft7Validator(schema)


def _error_text(error) -> str:
    path = ".".join(str(part) for part in error.path)
    location = path or "(root)"
    return f"{location}: {error.message}"


def validate_state(state, schema: dict = None) -> list:
    """Validate a state instance against the schema.

    Args:
        state: A parsed JSON object (dict) representing a learning-state instance.
        schema: Optional schema dict. Defaults to the repository schema.

    Returns:
        A list of human-readable validation error strings. An empty list means
        the instance is valid. No exceptions are raised for invalid content;
        callers distinguish validity via the returned list.
    """
    if schema is None:
        schema = load_schema()
    if not isinstance(state, dict):
        return [f"(root): state must be a JSON object, got {type(state).__name__}"]
    validator = _make_validator(schema)
    errors = sorted(validator.iter_errors(state), key=lambda e: list(e.path))
    return [_error_text(error) for error in errors]


def is_valid_state(state, schema: dict = None) -> bool:
    """Return True when the state instance is schema-valid, False otherwise."""
    return not validate_state(state, schema)


def save_state(state, filepath, schema: dict = None) -> Path:
    """Validate and persist a state instance as JSON.

    The instance is fully validated before anything is written. An invalid
    instance raises LearningStateError and no file is created or modified
    (no silent repair, no partial write).

    Writes are atomic: content is written to a temporary file in the same
    directory as the target and moved into place with os.replace() only after
    the temporary file is fully written and closed. If any step fails, the
    temporary file is removed and an existing target file is left unchanged.

    Args:
        state: A learning-state instance (dict) to persist.
        filepath: Destination file path (str or Path).
        schema: Optional schema dict. Defaults to the repository schema.

    Returns:
        The resolved destination Path on success.

    Raises:
        LearningStateError: If the instance is invalid or the file cannot be written.
    """
    errors = validate_state(state, schema)
    if errors:
        raise LearningStateError("state invalid; not saved:\n- " + "\n- ".join(errors))

    path = Path(filepath)
    try:
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
    except (OSError, TypeError) as exc:
        raise LearningStateError(
            f"failed to create a temporary file next to {path}: {exc}"
        ) from exc
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp_path, path)
    except (OSError, TypeError) as exc:
        raise LearningStateError(f"failed to write state to {path}: {exc}") from exc
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass
    return path


def load_state(filepath, schema: dict = None) -> dict:
    """Load, parse, and validate a state file.

    Args:
        filepath: Path of the state JSON file to read.
        schema: Optional schema dict. Defaults to the repository schema.

    Returns:
        The parsed state instance (dict).

    Raises:
        LearningStateError: If the file is unreadable, its content is malformed
            JSON, or the parsed instance fails schema validation.
    """
    path = Path(filepath)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LearningStateError(f"failed to read state file {path}: {exc}") from exc

    try:
        state = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LearningStateError(f"malformed JSON in {path}: {exc}") from exc

    errors = validate_state(state, schema)
    if errors:
        raise LearningStateError(f"state in {path} is invalid:\n- " + "\n- ".join(errors))
    return state


__all__ = [
    "LearningStateError",
    "default_schema_path",
    "load_schema",
    "validate_state",
    "is_valid_state",
    "save_state",
    "load_state",
]
