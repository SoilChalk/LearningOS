#!/usr/bin/env bash
#
# Negative tests for control state consistency checker
#
# Proves the production checker rejects:
# - Positive fixture test: valid control state passes
# - 1. CURRENT_TASK status is not awaiting_owner_decision
# - 2-9. Each of the eight lifecycle field mismatches
#
# All tests operate on temporary fixture copies. The production checker
# is invoked with --current-task, --current-state, and --task-result options.
# Before/after hashes prove live authority files remain unchanged.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CHECKER="$SCRIPT_DIR/check_control_state.py"

# Create temporary fixture directory
FIXTURE_DIR=$(mktemp -d)
trap "rm -rf '$FIXTURE_DIR'" EXIT

# Copy authority files to fixtures
cp "$REPO_ROOT/agent-control/CURRENT_TASK.yaml" "$FIXTURE_DIR/CURRENT_TASK.yaml"
cp "$REPO_ROOT/state/CURRENT_STATE.yaml" "$FIXTURE_DIR/CURRENT_STATE.yaml"
cp "$REPO_ROOT/agent-control/results/task-001.json" "$FIXTURE_DIR/task-001.json"

# Record hashes of live authority files before tests
HASH_BEFORE_TASK=$(shasum -a 256 "$REPO_ROOT/agent-control/CURRENT_TASK.yaml" | awk '{print $1}')
HASH_BEFORE_STATE=$(shasum -a 256 "$REPO_ROOT/state/CURRENT_STATE.yaml" | awk '{print $1}')
HASH_BEFORE_RESULT=$(shasum -a 256 "$REPO_ROOT/agent-control/results/task-001.json" | awk '{print $1}')

test_count=0
pass_count=0

run_positive_test() {
    local test_name="$1"

    test_count=$((test_count + 1))

    # Run checker on valid fixtures - should pass
    if python3 "$CHECKER" \
        --current-task "$FIXTURE_DIR/CURRENT_TASK.yaml" \
        --current-state "$FIXTURE_DIR/CURRENT_STATE.yaml" \
        --task-result "$FIXTURE_DIR/task-001.json" >/dev/null 2>&1; then
        echo "✓ Test $test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        return 0
    else
        echo "✗ Test $test_count FAILED: $test_name (checker rejected valid state)"
        return 1
    fi
}

run_negative_test() {
    local test_name="$1"
    local modify_fn="$2"

    test_count=$((test_count + 1))

    # Restore original fixtures
    cp "$REPO_ROOT/agent-control/CURRENT_TASK.yaml" "$FIXTURE_DIR/CURRENT_TASK.yaml"
    cp "$REPO_ROOT/state/CURRENT_STATE.yaml" "$FIXTURE_DIR/CURRENT_STATE.yaml"
    cp "$REPO_ROOT/agent-control/results/task-001.json" "$FIXTURE_DIR/task-001.json"

    # Apply modification to fixtures
    eval "$modify_fn"

    # Run checker - should fail
    if python3 "$CHECKER" \
        --current-task "$FIXTURE_DIR/CURRENT_TASK.yaml" \
        --current-state "$FIXTURE_DIR/CURRENT_STATE.yaml" \
        --task-result "$FIXTURE_DIR/task-001.json" >/dev/null 2>&1; then
        echo "✗ Test $test_count FAILED: $test_name (checker did not reject invalid state)"
        return 1
    else
        echo "✓ Test $test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        return 0
    fi
}

# Positive test: valid fixtures should pass
run_positive_test "Valid control state passes"

# Test 1: CURRENT_TASK status is not awaiting_owner_decision
run_negative_test "CURRENT_TASK status not awaiting_owner_decision" "
    sed -i.bak 's/^status: .*$/status: ready/' \
        '$FIXTURE_DIR/CURRENT_TASK.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'
"

# Test 2: previous_agent_execution mismatch
run_negative_test "previous_agent_execution mismatch" "
    sed -i.bak 's/previous_agent_execution: cancelled_after_commit_and_push/previous_agent_execution: completed/' \
        '$FIXTURE_DIR/CURRENT_TASK.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'
"

# Test 3: technical_completion mismatch
run_negative_test "technical_completion mismatch" "
    sed -i.bak 's/technical_completion: candidate_complete/technical_completion: in_progress/' \
        '$FIXTURE_DIR/CURRENT_STATE.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'
"

# Test 4: reviewer_acceptance mismatch
run_negative_test "reviewer_acceptance mismatch" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['reviewer_acceptance'] = 'pending'
with open('$FIXTURE_DIR/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Test 5: latest_reviewer_record mismatch
run_negative_test "latest_reviewer_record mismatch" "
    sed -i.bak 's/latest_reviewer_record: task-001-review-12/latest_reviewer_record: task-001-review-11/' \
        '$FIXTURE_DIR/CURRENT_TASK.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'
"

# Test 6: owner_acceptance mismatch
run_negative_test "owner_acceptance mismatch" "
    sed -i.bak 's/owner_acceptance: pending/owner_acceptance: accepted/' \
        '$FIXTURE_DIR/CURRENT_STATE.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'
"

# Test 7: lifecycle_status mismatch
run_negative_test "lifecycle_status mismatch" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['lifecycle_status'] = 'complete'
with open('$FIXTURE_DIR/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Test 8: formal_closure mismatch
run_negative_test "formal_closure mismatch" "
    sed -i.bak 's/formal_closure: false/formal_closure: true/' \
        '$FIXTURE_DIR/CURRENT_TASK.yaml'
    rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'
"

# Test 9: task_002_status mismatch
run_negative_test "task_002_status mismatch" "
    python3 -c \"
import json
with open('$FIXTURE_DIR/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['task_002_status'] = 'in_progress'
with open('$FIXTURE_DIR/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Verify live authority files unchanged
HASH_AFTER_TASK=$(shasum -a 256 "$REPO_ROOT/agent-control/CURRENT_TASK.yaml" | awk '{print $1}')
HASH_AFTER_STATE=$(shasum -a 256 "$REPO_ROOT/state/CURRENT_STATE.yaml" | awk '{print $1}')
HASH_AFTER_RESULT=$(shasum -a 256 "$REPO_ROOT/agent-control/results/task-001.json" | awk '{print $1}')

echo ""
echo "=== Live authority file integrity ==="
if [ "$HASH_BEFORE_TASK" = "$HASH_AFTER_TASK" ] && \
   [ "$HASH_BEFORE_STATE" = "$HASH_AFTER_STATE" ] && \
   [ "$HASH_BEFORE_RESULT" = "$HASH_AFTER_RESULT" ]; then
    echo "✓ All live authority files unchanged"
else
    echo "✗ ERROR: Live authority files were modified!"
    echo "  CURRENT_TASK.yaml: $HASH_BEFORE_TASK -> $HASH_AFTER_TASK"
    echo "  CURRENT_STATE.yaml: $HASH_BEFORE_STATE -> $HASH_AFTER_STATE"
    echo "  task-001.json: $HASH_BEFORE_RESULT -> $HASH_AFTER_RESULT"
    exit 1
fi

# Summary
echo ""
echo "=== Negative test summary ==="
echo "Tests run: $test_count"
echo "Tests passed: $pass_count"

if [ "$pass_count" -eq "$test_count" ] && [ "$test_count" -eq 10 ]; then
    echo "✓ All $test_count tests passed (1 positive + 9 negative)"
    exit 0
else
    echo "✗ Some tests failed or insufficient coverage (need 10, have $pass_count/$test_count)"
    exit 1
fi
