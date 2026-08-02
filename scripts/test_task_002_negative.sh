#!/usr/bin/env bash
#
# Task 002 Negative Test Suite
#
# Proves the Task 002 validator correctly rejects invalid design artifacts.
# All tests operate on temporary fixture copies. The production validator
# is invoked with modified fixtures. Before/after hashes prove live files
# remain unchanged.
#
# Negative test cases:
# 1. Scenario document missing required section
# 2. Decision tree missing classification type
# 3. State schema with prohibited field (knowledge_graph)
# 4. State schema evidence_level includes level 3 (mastery inference)
# 5. State schema additionalProperties not false
# 6. Scenario does not reference decision tree
# 7. Scenario has wrong number of flow steps
# 8. Decision tree does not acknowledge provisional status

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR="$SCRIPT_DIR/validate_task_002.py"

# Create temporary fixture directory
FIXTURE_DIR=$(mktemp -d)
trap "rm -rf '$FIXTURE_DIR'" EXIT

# Create fixture copies
mkdir -p "$FIXTURE_DIR/docs" "$FIXTURE_DIR/templates" "$FIXTURE_DIR/scripts"
cp "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
cp "$REPO_ROOT/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
cp "$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json" "$FIXTURE_DIR/templates/" 2>/dev/null || true
cp "$REPO_ROOT/scripts/validate_task_002.py" "$FIXTURE_DIR/scripts/"

# Record hashes of live files before tests
HASH_BEFORE_SCENARIO=$(shasum -a 256 "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" 2>/dev/null | awk '{print $1}' || echo "")
HASH_BEFORE_TREE=$(shasum -a 256 "$REPO_ROOT/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md" 2>/dev/null | awk '{print $1}' || echo "")
HASH_BEFORE_SCHEMA=$(shasum -a 256 "$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json" 2>/dev/null | awk '{print $1}' || echo "")

test_count=0
pass_count=0

run_positive_test() {
    local test_name="$1"
    
    test_count=$((test_count + 1))
    
    # Run validator on valid fixtures - should pass
    cd "$FIXTURE_DIR"
    if python3 scripts/validate_task_002.py >/dev/null 2>&1; then
        echo "✓ Test $test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        cd "$REPO_ROOT"
        return 0
    else
        echo "✗ Test $test_count FAILED: $test_name (validator rejected valid state)"
        cd "$REPO_ROOT"
        return 1
    fi
}

run_negative_test() {
    local test_name="$1"
    local modify_fn="$2"

    test_count=$((test_count + 1))

    # Restore original fixtures
    cp "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
    cp "$REPO_ROOT/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
    cp "$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json" "$FIXTURE_DIR/templates/" 2>/dev/null || true

    # Apply modification to fixtures
    eval "$modify_fn"

    # Run validator - should fail
    cd "$FIXTURE_DIR"
    if python3 scripts/validate_task_002.py >/dev/null 2>&1; then
        echo "✗ Test $test_count FAILED: $test_name (validator did not reject invalid state)"
        cd "$REPO_ROOT"
        return 1
    else
        echo "✓ Test $test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        cd "$REPO_ROOT"
        return 0
    fi
}

# Positive test: valid fixtures should pass
if [ -f "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" ]; then
    run_positive_test "Valid design artifacts pass"
else
    echo "⊘ Test 1 skipped: Design artifacts not yet created"
    test_count=$((test_count + 1))
fi

# Test 1: Scenario document missing required section
run_negative_test "Scenario missing required section" "
    sed -i.bak '/## Measurable Success Criteria/,/^## /d' '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md'
    rm -f '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md.bak'
"

# Test 2: Decision tree missing classification type
run_negative_test "Decision tree missing classification type" "
    sed -i.bak 's/terminology_gap/REMOVED_TYPE/g' '$FIXTURE_DIR/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md'
    rm -f '$FIXTURE_DIR/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md.bak'
"

# Test 3: State schema with prohibited field (knowledge_graph)
run_negative_test "State schema with prohibited knowledge_graph field" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
schema['properties']['knowledge_graph'] = {'type': 'object'}
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# Test 4: State schema evidence_level includes level 3 (mastery)
run_negative_test "State schema evidence_level includes mastery level 3" "
    sed -i.bak 's/\"enum\": \[0, 1, 2\]/\"enum\": [0, 1, 2, 3]/g' '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json'
    rm -f '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json.bak'
"

# Test 5: State schema additionalProperties not false
run_negative_test "State schema additionalProperties not false" "
    sed -i.bak 's/\"additionalProperties\": false/\"additionalProperties\": true/g' '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json'
    rm -f '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json.bak'
"

# Test 6: Scenario does not reference decision tree
run_negative_test "Scenario missing decision tree reference" "
    sed -i.bak 's/PEDAGOGICAL_ACTION_DECISION_TREE.md/REMOVED_REFERENCE/g' '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md'
    rm -f '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md.bak'
"

# Test 7: Scenario has wrong number of flow steps (delete Step 5)
run_negative_test "Scenario missing flow step" "
    sed -i.bak '/### Step 5:/,/^### Step 6:/d' '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md'
    rm -f '$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md.bak'
"

# Test 8: Decision tree does not acknowledge provisional status
run_negative_test "Decision tree missing provisional status" "
    sed -i.bak 's/provisional/REMOVED_STATUS/gi' '$FIXTURE_DIR/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md'
    rm -f '$FIXTURE_DIR/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md.bak'
"

# Verify live files unchanged
HASH_AFTER_SCENARIO=$(shasum -a 256 "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" 2>/dev/null | awk '{print $1}' || echo "")
HASH_AFTER_TREE=$(shasum -a 256 "$REPO_ROOT/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md" 2>/dev/null | awk '{print $1}' || echo "")
HASH_AFTER_SCHEMA=$(shasum -a 256 "$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json" 2>/dev/null | awk '{print $1}' || echo "")

echo ""
echo "=== Live file integrity ==="
if [ "$HASH_BEFORE_SCENARIO" = "$HASH_AFTER_SCENARIO" ] && \
   [ "$HASH_BEFORE_TREE" = "$HASH_AFTER_TREE" ] && \
   [ "$HASH_BEFORE_SCHEMA" = "$HASH_AFTER_SCHEMA" ]; then
    echo "✓ All live design files unchanged"
else
    echo "✗ ERROR: Live design files were modified!"
    echo "  FIRST_VERTICAL_SCENARIO.md: $HASH_BEFORE_SCENARIO -> $HASH_AFTER_SCENARIO"
    echo "  PEDAGOGICAL_ACTION_DECISION_TREE.md: $HASH_BEFORE_TREE -> $HASH_AFTER_TREE"
    echo "  MINIMAL_LEARNING_STATE.schema.json: $HASH_BEFORE_SCHEMA -> $HASH_AFTER_SCHEMA"
    exit 1
fi

# Summary
echo ""
echo "=== Negative test summary ==="
echo "Tests run: $test_count"
echo "Tests passed: $pass_count"

if [ "$pass_count" -eq "$test_count" ] && [ "$test_count" -ge 9 ]; then
    echo "✓ All $test_count tests passed (1 positive + 8 negative)"
    exit 0
else
    echo "✗ Some tests failed or insufficient coverage (need 9, have $pass_count/$test_count)"
    exit 1
fi
