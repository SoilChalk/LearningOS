#!/bin/bash
# Negative test: prove that invalid ledger/record causes production validator to exit nonzero

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Running negative validation tests ==="

# Test 1: Invalid ledger with missing required field 'status'
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

if python3 scripts/validate_source_records.py --ledger "$INVALID_LEDGER" 2>/dev/null; then
    echo "FAIL: Invalid ledger passed validation" >&2
    rm -f "$INVALID_LEDGER"
    exit 1
else
    echo "✓ Invalid ledger correctly rejected (production validator returned nonzero)"
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

if python3 scripts/validate_source_records.py --record "$INVALID_RECORD" 2>/dev/null; then
    echo "FAIL: Invalid ID pattern passed validation" >&2
    rm -f "$INVALID_RECORD"
    exit 1
else
    echo "✓ Invalid ID pattern correctly rejected (production validator returned nonzero)"
fi
rm -f "$INVALID_RECORD"

# Test 3: Invalid source record with malformed date
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

if python3 scripts/validate_source_records.py --record "$INVALID_DATE" 2>/dev/null; then
    echo "FAIL: Invalid date passed validation" >&2
    rm -f "$INVALID_DATE"
    exit 1
else
    echo "✓ Invalid date correctly rejected (production validator returned nonzero)"
fi
rm -f "$INVALID_DATE"

echo ""
echo "=== All negative tests passed ==="
echo "    (Production validator correctly returned nonzero for all invalid inputs)"
exit 0
