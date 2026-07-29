#!/usr/bin/env python3
"""
Validate source ledger and individual source records using JSON Schema.
Returns 0 on success, nonzero on validation failure.
"""

import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError, RefResolver
except ImportError:
    print("ERROR: jsonschema library not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

def validate_source_ledger():
    """Validate source ledger and records using actual JSON Schema validation."""
    repo_root = Path(__file__).parent.parent
    ledger_path = repo_root / "sources" / "source-ledger.json"
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
    
    # Set up resolver for $ref
    schema_store = {
        ledger_schema.get("$id", str(ledger_schema_path.resolve())): ledger_schema,
        record_schema.get("$id", str(record_schema_path.resolve())): record_schema,
        "./SOURCE_RECORD.json": record_schema,
        "../templates/SOURCE_RECORD.json": record_schema
    }
    resolver = RefResolver.from_schema(ledger_schema, store=schema_store)
    
    # Validate ledger against ledger schema
    try:
        validate(instance=ledger, schema=ledger_schema, resolver=resolver)
        print("✓ Ledger structure validated against SOURCE_LEDGER.schema.json")
    except ValidationError as e:
        print(f"VALIDATION FAILED: Ledger structure invalid", file=sys.stderr)
        print(f"  Path: {' -> '.join(str(p) for p in e.path)}", file=sys.stderr)
        print(f"  Error: {e.message}", file=sys.stderr)
        return 1
    
    # Validate each source record
    source_count = len(ledger.get("sources", []))
    for i, source in enumerate(ledger.get("sources", [])):
        source_id = source.get("id", f"source_{i}")
        try:
            validate(instance=source, schema=record_schema)
        except ValidationError as e:
            print(f"VALIDATION FAILED: {source_id} invalid", file=sys.stderr)
            print(f"  Path: {' -> '.join(str(p) for p in e.path)}", file=sys.stderr)
            print(f"  Error: {e.message}", file=sys.stderr)
            return 1
    
    print(f"✓ {source_count} source records validated against SOURCE_RECORD.json")
    return 0

if __name__ == "__main__":
    sys.exit(validate_source_ledger())
