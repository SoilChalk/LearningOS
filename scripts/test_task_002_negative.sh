#!/usr/bin/env bash
#
# Task 002 Test Suite (Protocol 19)
#
# Validates Task 002 design artifacts through structural and instance-level tests.
# All tests operate on temporary fixture copies. Before/after hashes prove live
# files remain unchanged.
#
# Test Coverage (26 total: 4 positive + 22 negative):
#   Structural Tests (20 total: 1 positive + 19 negative):
#     - Scenario document structure and flow steps
#     - Decision tree classification and action types
#     - State schema constraints and prohibited fields
#     - Cross-document consistency
#
#   Instance Validation Tests (6 total: 3 positive + 3 negative):
#     - cannot_articulate + null obstacle + in_scope + request_explanation + citations (positive)
#     - stop + missing_required_material + empty citations + stop_reason (positive)
#     - stop + outside_supplied_corpus + empty citations + stop_reason (positive)
#     - stop + in_scope + empty citations + stop_reason - INVALID (negative)
#     - stop + missing_required_material + empty citations + NO stop_reason - INVALID (negative)
#     - request_explanation + empty citations - INVALID (negative)
#
# Instance tests use jsonschema.Draft7Validator to validate complete minimal
# learning state instances against the actual schema.

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

# Test counters - machine-derived from actual test execution
positive_test_count=0
negative_test_count=0
structural_test_count=0
instance_test_count=0
total_test_count=0
pass_count=0

# Track test results by name
declare -a test_results

run_positive_test() {
    local test_name="$1"
    
    positive_test_count=$((positive_test_count + 1))
    structural_test_count=$((structural_test_count + 1))
    total_test_count=$((total_test_count + 1))
    
    # Run validator on valid fixtures - should pass
    cd "$FIXTURE_DIR"
    if python3 scripts/validate_task_002.py >/dev/null 2>&1; then
        echo "✓ Test $total_test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        test_results+=("PASS: $test_name")
        cd "$REPO_ROOT"
        return 0
    else
        echo "✗ Test $total_test_count FAILED: $test_name (validator rejected valid state)"
        test_results+=("FAIL: $test_name")
        cd "$REPO_ROOT"
        return 1
    fi
}

run_negative_test() {
    local test_name="$1"
    local modify_fn="$2"

    negative_test_count=$((negative_test_count + 1))
    structural_test_count=$((structural_test_count + 1))
    total_test_count=$((total_test_count + 1))

    # Restore original fixtures
    cp "$REPO_ROOT/docs/FIRST_VERTICAL_SCENARIO.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
    cp "$REPO_ROOT/docs/PEDAGOGICAL_ACTION_DECISION_TREE.md" "$FIXTURE_DIR/docs/" 2>/dev/null || true
    cp "$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json" "$FIXTURE_DIR/templates/" 2>/dev/null || true

    # Apply modification to fixtures
    eval "$modify_fn"

    # Run validator - should fail
    cd "$FIXTURE_DIR"
    if python3 scripts/validate_task_002.py >/dev/null 2>&1; then
        echo "✗ Test $total_test_count FAILED: $test_name (validator did not reject invalid state)"
        test_results+=("FAIL: $test_name")
        cd "$REPO_ROOT"
        return 1
    else
        echo "✓ Test $total_test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        test_results+=("PASS: $test_name")
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

# Test 9: Step 1 missing Entry Criteria
run_negative_test "Step 1 missing Entry Criteria" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
# Find Step 1 section
step1_start = content.find('### Step 1:')
step2_start = content.find('### Step 2:', step1_start)
# Remove **Entry Criteria** line from Step 1
step1_section = content[step1_start:step2_start]
step1_modified = step1_section.replace('**Entry Criteria**', '**REMOVED_CRITERIA**', 1)
new_content = content[:step1_start] + step1_modified + content[step2_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 10: Step 2 missing Exit Criteria
run_negative_test "Step 2 missing Exit Criteria" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
step2_start = content.find('### Step 2:')
step3_start = content.find('### Step 3:', step2_start)
step2_section = content[step2_start:step3_start]
step2_modified = step2_section.replace('**Exit Criteria**', '**REMOVED_CRITERIA**', 1)
new_content = content[:step2_start] + step2_modified + content[step3_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 11: Step 3 missing Recovery Behavior
run_negative_test "Step 3 missing Recovery Behavior" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
step3_start = content.find('### Step 3:')
step4_start = content.find('### Step 4:', step3_start)
step3_section = content[step3_start:step4_start]
step3_modified = step3_section.replace('**Recovery Behavior**', '**REMOVED_BEHAVIOR**', 1)
new_content = content[:step3_start] + step3_modified + content[step4_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 12: Step 4 missing Evidence Collection
run_negative_test "Step 4 missing Evidence Collection" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
step4_start = content.find('### Step 4:')
step5_start = content.find('### Step 5:', step4_start)
step4_section = content[step4_start:step5_start]
step4_modified = step4_section.replace('**Evidence Collection**', '**REMOVED_COLLECTION**', 1)
new_content = content[:step4_start] + step4_modified + content[step5_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 13: Step 5 missing Entry Criteria
run_negative_test "Step 5 missing Entry Criteria" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
step5_start = content.find('### Step 5:')
step6_start = content.find('### Step 6:', step5_start)
step5_section = content[step5_start:step6_start]
step5_modified = step5_section.replace('**Entry Criteria**', '**REMOVED_CRITERIA**', 1)
new_content = content[:step5_start] + step5_modified + content[step6_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 14: Step 6 missing Exit Criteria
run_negative_test "Step 6 missing Exit Criteria" "
    python3 -c \"
import re
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md') as f:
    content = f.read()
step6_start = content.find('### Step 6:')
flow_summary_start = content.find('## Complete Flow Summary', step6_start)
step6_section = content[step6_start:flow_summary_start]
step6_modified = step6_section.replace('**Exit Criteria**', '**REMOVED_CRITERIA**', 1)
new_content = content[:step6_start] + step6_modified + content[flow_summary_start:]
with open('$FIXTURE_DIR/docs/FIRST_VERTICAL_SCENARIO.md', 'w') as f:
    f.write(new_content)
\"
"

# Test 15: Source-grounded action with zero citations
run_negative_test "Source-grounded action with zero citations" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
# Remove the if/then citation constraint to simulate unconstrained schema
if 'if' in schema.get('properties', {}).get('last_pedagogical_action', {}):
    del schema['properties']['last_pedagogical_action']['if']
if 'then' in schema.get('properties', {}).get('last_pedagogical_action', {}):
    del schema['properties']['last_pedagogical_action']['then']
if 'else' in schema.get('properties', {}).get('last_pedagogical_action', {}):
    del schema['properties']['last_pedagogical_action']['else']
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# Test 17: Arbitrary property in bounded nested object
run_negative_test "Arbitrary property in bounded nested object" "
    sed -i.bak 's/\"additionalProperties\": false/\"additionalProperties\": true/' '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json'
    rm -f '$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json.bak'
"

# Test 18: Nullable type with enum omitting null
run_negative_test "Nullable type with enum omitting null" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
# Modify check_type to have type null but enum without null
check_type = schema['properties']['independent_check']['properties']['check_type']
check_type['type'] = ['string', 'null']
check_type['enum'] = ['explain_concept', 'solve_similar_problem', 'apply_to_example', 'none']  # Missing null
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# Test 19: cannot_articulate in core obstacle_classification enum
run_negative_test "cannot_articulate in core obstacle_classification enum" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
# Add cannot_articulate to obstacle_classification enum
obstacle_enum = schema['properties']['observed_difficulty']['properties']['obstacle_classification']['enum']
if 'cannot_articulate' not in obstacle_enum:
    obstacle_enum.insert(0, 'cannot_articulate')
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# Test 20: Undefined obstacle classification
run_negative_test "Undefined obstacle classification" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
# Add invalid classification to enum
obstacle_enum = schema['properties']['observed_difficulty']['properties']['obstacle_classification']['enum']
obstacle_enum.append('invalid_classification')
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# Test 21: Obsolete outside_corpus present
run_negative_test "Obsolete outside_corpus present in schema" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
    schema = json.load(f)
# Add outside_corpus field (obsolete from Protocol 17)
schema['properties']['observed_difficulty']['properties']['outside_corpus'] = {
    'type': 'boolean',
    'description': 'Obsolete field from Protocol 16'
}
with open('$FIXTURE_DIR/templates/MINIMAL_LEARNING_STATE.schema.json', 'w') as f:
    json.dump(schema, f, indent=2)
\"
"

# === INSTANCE VALIDATION TESTS (Protocol 19) ===
# These tests validate complete minimal learning state instances against the schema
# using jsonschema.Draft7Validator. They test positive and negative cases for:
# - cannot_articulate classification
# - cross-object stop-action rules
# - source-grounded action citation requirements

run_instance_test() {
    local test_type="$1"  # "positive" or "negative"
    local test_name="$2"
    local instance_json="$3"
    
    if [ "$test_type" = "positive" ]; then
        positive_test_count=$((positive_test_count + 1))
    else
        negative_test_count=$((negative_test_count + 1))
    fi
    instance_test_count=$((instance_test_count + 1))
    total_test_count=$((total_test_count + 1))
    
    # Run validation using jsonschema.Draft7Validator
    set +e  # Temporarily disable exit on error
    result=$(python3 - <<PY
import json
import sys
try:
    import jsonschema
    
    with open('$REPO_ROOT/templates/MINIMAL_LEARNING_STATE.schema.json') as f:
        schema = json.load(f)
    
    instance = json.loads('''$instance_json''')
    
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(instance))
    
    if errors:
        sys.exit(1)  # INVALID
    else:
        sys.exit(0)  # VALID
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(2)
PY
)
    exit_code=$?
    set -e  # Re-enable exit on error
    
    if [ "$test_type" = "positive" ]; then
        # Positive test: should be VALID (exit 0)
        if [ $exit_code -eq 0 ]; then
            echo "✓ Test $total_test_count passed: $test_name (VALID as expected)"
            pass_count=$((pass_count + 1))
            test_results+=("PASS: $test_name")
            return 0
        else
            echo "✗ Test $total_test_count FAILED: $test_name (expected VALID, got INVALID)"
            test_results+=("FAIL: $test_name")
            return 1
        fi
    else
        # Negative test: should be INVALID (exit 1)
        if [ $exit_code -eq 1 ]; then
            echo "✓ Test $total_test_count passed: $test_name (INVALID as expected)"
            pass_count=$((pass_count + 1))
            test_results+=("PASS: $test_name")
            return 0
        else
            echo "✗ Test $total_test_count FAILED: $test_name (expected INVALID, got VALID)"
            test_results+=("FAIL: $test_name")
            return 1
        fi
    fi
}

echo ""
echo "=== Instance Validation Tests (Protocol 19) ==="

# Instance Positive A: cannot_articulate + null obstacle + in_scope + request_explanation + citations
positive_a=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T10:00:00Z",
  "created_at": "2026-08-05T10:00:00+08:00",
  "updated_at": "2026-08-05T10:05:00+08:00",
  "current_position": {
    "material_file": "course.pdf",
    "section": "Chapter 3",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T10:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "understand_concept",
    "scope_description": "Understand heap data structure",
    "completion_criterion": "Explain heap operations independently"
  },
  "observed_difficulty": {
    "user_statement": "I don't know what's confusing",
    "obstacle_classification": null,
    "material_scope_status": "in_scope",
    "articulation_status": "cannot_articulate",
    "expressed_at": "2026-08-05T10:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "request_explanation",
    "material_citations": [
      {
        "file": "course.pdf",
        "section": "Chapter 3"
      }
    ],
    "delivered_at": "2026-08-05T10:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Continue from current position",
    "rationale": "evidence_level_0_continue_from_current"
  }
}
JSON
)
run_instance_test "positive" "Instance Positive A: cannot_articulate + null obstacle + in_scope + request_explanation + citations" "$positive_a"

# Instance Positive B: stop + missing_required_material + empty citations + stop_reason
positive_b=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T11:00:00Z",
  "created_at": "2026-08-05T11:00:00+08:00",
  "updated_at": "2026-08-05T11:05:00+08:00",
  "current_position": {
    "material_file": "textbook.pdf",
    "section": "Chapter 5",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T11:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "solve_problem",
    "scope_description": "Solve dynamic programming problem",
    "completion_criterion": "Solve similar problem independently"
  },
  "observed_difficulty": {
    "user_statement": "Material doesn't cover memoization",
    "obstacle_classification": "prerequisite_deficit",
    "material_scope_status": "missing_required_material",
    "articulation_status": "articulated",
    "expressed_at": "2026-08-05T11:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "stop_and_request_more_material",
    "action_details": {
      "stop_reason": "Memoization prerequisite not covered in uploaded material"
    },
    "material_citations": [],
    "delivered_at": "2026-08-05T11:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Request material on memoization",
    "rationale": "escalation_threshold_review_offline"
  }
}
JSON
)
run_instance_test "positive" "Instance Positive B: stop + missing_required_material + empty citations + stop_reason" "$positive_b"

# Instance Positive C: stop + outside_supplied_corpus + empty citations + stop_reason
positive_c=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T12:00:00Z",
  "created_at": "2026-08-05T12:00:00+08:00",
  "updated_at": "2026-08-05T12:05:00+08:00",
  "current_position": {
    "material_file": "notes.pdf",
    "section": "Lecture 2",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T12:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "understand_concept",
    "scope_description": "Understand distributed consensus",
    "completion_criterion": "Explain Raft algorithm"
  },
  "observed_difficulty": {
    "user_statement": "Question about Paxos which isn't in the material",
    "obstacle_classification": "lost_context",
    "material_scope_status": "outside_supplied_corpus",
    "articulation_status": "articulated",
    "expressed_at": "2026-08-05T12:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "stop_and_request_more_material",
    "action_details": {
      "stop_reason": "Paxos algorithm not covered in uploaded corpus"
    },
    "material_citations": [],
    "delivered_at": "2026-08-05T12:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Request material on Paxos or refocus on Raft",
    "rationale": "escalation_threshold_review_offline"
  }
}
JSON
)
run_instance_test "positive" "Instance Positive C: stop + outside_supplied_corpus + empty citations + stop_reason" "$positive_c"

# Instance Negative A: stop + in_scope + empty citations + stop_reason (INVALID - material is in_scope)
negative_a=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T13:00:00Z",
  "created_at": "2026-08-05T13:00:00+08:00",
  "updated_at": "2026-08-05T13:05:00+08:00",
  "current_position": {
    "material_file": "book.pdf",
    "section": "Chapter 1",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T13:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "solve_problem",
    "scope_description": "Solve sorting problem",
    "completion_criterion": "Implement quicksort"
  },
  "observed_difficulty": {
    "user_statement": "Don't understand pivot selection",
    "obstacle_classification": "procedural_confusion",
    "material_scope_status": "in_scope",
    "articulation_status": "articulated",
    "expressed_at": "2026-08-05T13:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "stop_and_request_more_material",
    "action_details": {
      "stop_reason": "Need more examples"
    },
    "material_citations": [],
    "delivered_at": "2026-08-05T13:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Request more material",
    "rationale": "escalation_threshold_review_offline"
  }
}
JSON
)
run_instance_test "negative" "Instance Negative A: stop + in_scope + empty citations + stop_reason (invalid - material is in_scope)" "$negative_a"

# Instance Negative B: stop + missing_required_material + empty citations + NO stop_reason
negative_b=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T14:00:00Z",
  "created_at": "2026-08-05T14:00:00+08:00",
  "updated_at": "2026-08-05T14:05:00+08:00",
  "current_position": {
    "material_file": "slides.pdf",
    "section": "Slide 10",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T14:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "understand_concept",
    "scope_description": "Understand B-trees",
    "completion_criterion": "Explain B-tree operations"
  },
  "observed_difficulty": {
    "user_statement": "Missing prerequisite on balanced trees",
    "obstacle_classification": "prerequisite_deficit",
    "material_scope_status": "missing_required_material",
    "articulation_status": "articulated",
    "expressed_at": "2026-08-05T14:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "stop_and_request_more_material",
    "action_details": {},
    "material_citations": [],
    "delivered_at": "2026-08-05T14:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Request balanced tree material",
    "rationale": "escalation_threshold_review_offline"
  }
}
JSON
)
run_instance_test "negative" "Instance Negative B: stop + missing_required_material + empty citations + NO stop_reason" "$negative_b"

# Instance Negative C: request_explanation + empty citations (source-grounded action without citations)
negative_c=$(cat <<'JSON'
{
  "schema_version": "1.0",
  "scenario_id": "source-grounded-learning-recovery-and-independent-completion-check",
  "session_id": "session-2026-08-05T15:00:00Z",
  "created_at": "2026-08-05T15:00:00+08:00",
  "updated_at": "2026-08-05T15:05:00+08:00",
  "current_position": {
    "material_file": "manual.pdf",
    "section": "Section 2.3",
    "confirmed_by_user": true,
    "confirmed_at": "2026-08-05T15:01:00+08:00"
  },
  "task_boundary": {
    "task_type": "apply_to_example",
    "scope_description": "Apply merge sort to example",
    "completion_criterion": "Trace merge sort execution"
  },
  "observed_difficulty": {
    "user_statement": "Confused about merge step",
    "obstacle_classification": "procedural_confusion",
    "material_scope_status": "in_scope",
    "articulation_status": "articulated",
    "expressed_at": "2026-08-05T15:03:00+08:00"
  },
  "last_pedagogical_action": {
    "action_type": "request_explanation",
    "material_citations": [],
    "delivered_at": "2026-08-05T15:04:00+08:00"
  },
  "independent_check": {
    "requested": false,
    "evidence_level": 0
  },
  "next_action": {
    "recommendation": "Retry after explanation",
    "rationale": "evidence_level_0_continue_from_current"
  }
}
JSON
)
run_instance_test "negative" "Instance Negative C: request_explanation + empty citations (source-grounded action without citations)" "$negative_c"

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
echo "=== Test Summary (Protocol 19) ==="
echo "Structural tests: $structural_test_count (1 positive + $((structural_test_count - 1)) negative)"
echo "Instance validation tests: $instance_test_count (3 positive + 3 negative)"
echo "Total tests: $total_test_count"
echo "Tests passed: $pass_count"
echo ""

if [ "$pass_count" -eq "$total_test_count" ] && [ "$structural_test_count" -ge 20 ] && [ "$instance_test_count" -ge 6 ]; then
    echo "✓ All $total_test_count tests passed"
    echo "  - Structural: $structural_test_count tests (1 positive + $((structural_test_count - 1)) negative)"
    echo "  - Instance validation: $instance_test_count tests (3 positive + 3 negative)"
    echo ""
    echo "=== Test Results by Name ==="
    for result in "${test_results[@]}"; do
        echo "  $result"
    done
    exit 0
else
    echo "✗ Tests failed"
    echo "  Expected: $structural_test_count structural + $instance_test_count instance = $total_test_count total"
    echo "  Passed: $pass_count/$total_test_count"
    exit 1
fi
