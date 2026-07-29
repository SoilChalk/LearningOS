#!/bin/bash
# Negative test: prove that invalid ledger/record causes nonzero exit

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Running negative validation tests ==="

# Test 1: Invalid ledger with missing required field
echo "Test 1: Invalid ledger (missing required field 'status')"
INVALID_LEDGER=$(mktemp)
cat > "$INVALID_LEDGER" << 'LEDGER_EOF'
{
  "$schema": "../templates/SOURCE_LEDGER.schema.json",
  "schema_version": "1.0",
  "generated_at": "2026-07-29T16:00:00Z",
  "task_id": "task-001-core-research",
  "stage": "stage_2_core_source_verification",
  "source_count": 0,
  "target_minimum": 8,
  "target_maximum": 15,
  "sources": []
}
LEDGER_EOF

python3 << PYTHON_EOF
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, RefResolver, FormatChecker

repo_root = Path("$REPO_ROOT")
ledger_schema_path = repo_root / "templates" / "SOURCE_LEDGER.schema.json"
record_schema_path = repo_root / "templates" / "SOURCE_RECORD.json"

with open(ledger_schema_path) as f:
    ledger_schema = json.load(f)
with open(record_schema_path) as f:
    record_schema = json.load(f)
with open("$INVALID_LEDGER") as f:
    ledger = json.load(f)

schema_store = {
    "./SOURCE_RECORD.json": record_schema,
    "../templates/SOURCE_RECORD.json": record_schema
}
resolver = RefResolver.from_schema(ledger_schema, store=schema_store)
format_checker = FormatChecker()

try:
    validate(instance=ledger, schema=ledger_schema, resolver=resolver, format_checker=format_checker)
    print("FAIL: Invalid ledger passed validation", file=sys.stderr)
    sys.exit(1)
except ValidationError:
    print("✓ Invalid ledger correctly rejected")
    sys.exit(0)
PYTHON_EOF

if [ $? -ne 0 ]; then
    echo "FAILED: Test 1"
    rm -f "$INVALID_LEDGER"
    exit 1
fi
rm -f "$INVALID_LEDGER"

# Test 2: Invalid source record with wrong ID pattern
echo "Test 2: Invalid source record (wrong ID pattern)"
INVALID_RECORD=$(mktemp)
cat > "$INVALID_RECORD" << 'RECORD_EOF'
{
  "id": "invalid-id",
  "title": "Test Source",
  "organization_or_authors": "Test Org",
  "publication_date": "2026",
  "source_type": "product_documentation",
  "url": "https://example.com/test",
  "accessed_at": "2026-07-29",
  "research_question_ids": ["RQ1.1"],
  "directly_supported_observations": ["Test observation"],
  "design_implications": ["Test implication"],
  "limitations_and_non_inferences": ["Test limitation"],
  "decision_affected": ["source_grounding_strategy"],
  "verification_status": "verified"
}
RECORD_EOF

python3 << PYTHON_EOF
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, FormatChecker

repo_root = Path("$REPO_ROOT")
record_schema_path = repo_root / "templates" / "SOURCE_RECORD.json"

with open(record_schema_path) as f:
    record_schema = json.load(f)
with open("$INVALID_RECORD") as f:
    record = json.load(f)

format_checker = FormatChecker()

try:
    validate(instance=record, schema=record_schema, format_checker=format_checker)
    print("FAIL: Invalid ID pattern passed validation", file=sys.stderr)
    sys.exit(1)
except ValidationError:
    print("✓ Invalid ID pattern correctly rejected")
    sys.exit(0)
PYTHON_EOF

if [ $? -ne 0 ]; then
    echo "FAILED: Test 2"
    rm -f "$INVALID_RECORD"
    exit 1
fi
rm -f "$INVALID_RECORD"

# Test 3: Invalid source record with bad date format
echo "Test 3: Invalid source record (malformed date)"
INVALID_DATE=$(mktemp)
cat > "$INVALID_DATE" << 'DATE_EOF'
{
  "id": "src-999",
  "title": "Test Source",
  "organization_or_authors": "Test Org",
  "publication_date": "2026",
  "source_type": "product_documentation",
  "url": "https://example.com/test",
  "accessed_at": "not-a-date",
  "research_question_ids": ["RQ1.1"],
  "directly_supported_observations": ["Test observation"],
  "design_implications": ["Test implication"],
  "limitations_and_non_inferences": ["Test limitation"],
  "decision_affected": ["source_grounding_strategy"],
  "verification_status": "verified"
}
DATE_EOF

python3 << PYTHON_EOF
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError, FormatChecker

repo_root = Path("$REPO_ROOT")
record_schema_path = repo_root / "templates" / "SOURCE_RECORD.json"

with open(record_schema_path) as f:
    record_schema = json.load(f)
with open("$INVALID_DATE") as f:
    record = json.load(f)

format_checker = FormatChecker()

try:
    validate(instance=record, schema=record_schema, format_checker=format_checker)
    print("FAIL: Invalid date passed validation", file=sys.stderr)
    sys.exit(1)
except ValidationError:
    print("✓ Invalid date correctly rejected")
    sys.exit(0)
PYTHON_EOF

if [ $? -ne 0 ]; then
    echo "FAILED: Test 3"
    rm -f "$INVALID_DATE"
    exit 1
fi
rm -f "$INVALID_DATE"

echo ""
echo "=== All negative tests passed ==="
exit 0
