#!/usr/bin/env python3
"""
Validate source ledger and individual source records using JSON Schema.
Returns 0 on success, nonzero on validation failure.

Usage:
  python3 scripts/validate_source_records.py                    # Validate repository ledger
  python3 scripts/validate_source_records.py --ledger PATH      # Validate specific ledger
  python3 scripts/validate_source_records.py --record PATH      # Validate specific record
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, RefResolver, FormatChecker
except ImportError:
    print("ERROR: jsonschema library not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

def validate_source_ledger(ledger_path=None):
    """Validate source ledger and records using actual JSON Schema validation with format checking."""
    repo_root = Path(__file__).parent.parent

    # Use provided path or default to repository ledger
    if ledger_path is None:
        ledger_path = repo_root / "sources" / "source-ledger.json"
    else:
        ledger_path = Path(ledger_path)

    ledger_schema_path = repo_root / "templates" / "SOURCE_LEDGER.schema.json"
    record_schema_path = repo_root / "templates" / "SOURCE_RECORD.json"

    # Load schemas
    try:
        with open(ledger_schema_path) as f:
            ledger_schema = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load ledger schema: {e}", file=sys.stderr)
        return 1

    try:
        with open(record_schema_path) as f:
            record_schema = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load record schema: {e}", file=sys.stderr)
        return 1

    # Load ledger
    try:
        with open(ledger_path) as f:
            ledger = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load source ledger: {e}", file=sys.stderr)
        return 1

    # Set up resolver for $ref with deterministic local resolution
    schema_store = {
        ledger_schema.get("$id", str(ledger_schema_path.resolve())): ledger_schema,
        record_schema.get("$id", str(record_schema_path.resolve())): record_schema,
        "./SOURCE_RECORD.json": record_schema,
        "../templates/SOURCE_RECORD.json": record_schema
    }
    resolver = RefResolver.from_schema(ledger_schema, store=schema_store)

    # Enable format checking for uri, date, date-time
    format_checker = FormatChecker()

    # Validate ledger against ledger schema with format checking
    try:
        validate(instance=ledger, schema=ledger_schema, resolver=resolver, format_checker=format_checker)
        print("✓ Ledger structure validated against SOURCE_LEDGER.schema.json")
    except ValidationError as e:
        print(f"VALIDATION FAILED: Ledger structure invalid", file=sys.stderr)
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}", file=sys.stderr)
        print(f"  Error: {e.message}", file=sys.stderr)
        return 1

    # Validate each source record with format checking
    source_count = len(ledger.get("sources", []))
    for i, source in enumerate(ledger.get("sources", [])):
        source_id = source.get("id", f"source_{i}")
        try:
            validate(instance=source, schema=record_schema, format_checker=format_checker)
        except ValidationError as e:
            print(f"VALIDATION FAILED: {source_id} invalid", file=sys.stderr)
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}", file=sys.stderr)
            print(f"  Error: {e.message}", file=sys.stderr)
            return 1

    print(f"✓ {source_count} source records validated against SOURCE_RECORD.json")
    return 0

def validate_source_record(record_path):
    """Validate a single source record using JSON Schema with format checking."""
    repo_root = Path(__file__).parent.parent
    record_schema_path = repo_root / "templates" / "SOURCE_RECORD.json"
    record_path = Path(record_path)

    # Load schema
    try:
        with open(record_schema_path) as f:
            record_schema = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load record schema: {e}", file=sys.stderr)
        return 1

    # Load record
    try:
        with open(record_path) as f:
            record = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load source record: {e}", file=sys.stderr)
        return 1

    # Enable format checking
    format_checker = FormatChecker()

    # Validate record
    try:
        validate(instance=record, schema=record_schema, format_checker=format_checker)
        print(f"✓ Source record validated against SOURCE_RECORD.json")
        return 0
    except ValidationError as e:
        print(f"VALIDATION FAILED: Source record invalid", file=sys.stderr)
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}", file=sys.stderr)
        print(f"  Error: {e.message}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate source ledger or record using JSON Schema')
    parser.add_argument('--ledger', metavar='PATH', help='Path to ledger JSON file to validate')
    parser.add_argument('--record', metavar='PATH', help='Path to source record JSON file to validate')

    args = parser.parse_args()

    if args.ledger and args.record:
        print("ERROR: Cannot specify both --ledger and --record", file=sys.stderr)
        sys.exit(1)

    if args.record:
        sys.exit(validate_source_record(args.record))
    else:
        sys.exit(validate_source_ledger(args.ledger))
