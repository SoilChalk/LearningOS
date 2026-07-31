#!/usr/bin/env bash
#
# Negative tests for control state consistency checker
#
# Proves the production checker rejects:
# 1. CURRENT_TASK status is not awaiting_owner_decision
# 2-9. Each of the eight lifecycle field mismatches
#
# The test creates temporary modified files and invokes the production
# checker against them. It does NOT duplicate the checker implementation.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CHECKER="$SCRIPT_DIR/check_control_state.py"

# Backup original files
BACKUP_DIR=$(mktemp -d)
trap "rm -rf '$BACKUP_DIR'" EXIT

cp "$REPO_ROOT/agent-control/CURRENT_TASK.yaml" "$BACKUP_DIR/"
cp "$REPO_ROOT/state/CURRENT_STATE.yaml" "$BACKUP_DIR/"
cp "$REPO_ROOT/agent-control/results/task-001.json" "$BACKUP_DIR/"

test_count=0
pass_count=0

run_negative_test() {
    local test_name="$1"
    local modify_fn="$2"

    test_count=$((test_count + 1))

    # Restore originals
    cp "$BACKUP_DIR/CURRENT_TASK.yaml" "$REPO_ROOT/agent-control/"
    cp "$BACKUP_DIR/CURRENT_STATE.yaml" "$REPO_ROOT/state/"
    cp "$BACKUP_DIR/task-001.json" "$REPO_ROOT/agent-control/results/"

    # Apply modification
    eval "$modify_fn"

    # Run checker - should fail
    if python3 "$CHECKER" >/dev/null 2>&1; then
        echo "✗ Test $test_count FAILED: $test_name (checker did not reject invalid state)"
        return 1
    else
        echo "✓ Test $test_count passed: $test_name"
        pass_count=$((pass_count + 1))
        return 0
    fi
}

# Test 1: CURRENT_TASK status is not awaiting_owner_decision
run_negative_test "CURRENT_TASK status not awaiting_owner_decision" "
    sed -i.bak 's/^status: awaiting_owner_decision$/status: ready/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 2: previous_agent_execution mismatch
run_negative_test "previous_agent_execution mismatch" "
    sed -i.bak 's/previous_agent_execution: cancelled_after_commit_and_push/previous_agent_execution: completed/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 3: technical_completion mismatch
run_negative_test "technical_completion mismatch" "
    sed -i.bak 's/technical_completion: candidate_complete/technical_completion: in_progress/' \
        '$REPO_ROOT/state/CURRENT_STATE.yaml'
"

# Test 4: reviewer_acceptance mismatch
run_negative_test "reviewer_acceptance mismatch" "
    python3 -c \"
import json
with open('$REPO_ROOT/agent-control/results/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['reviewer_acceptance'] = 'pending'
with open('$REPO_ROOT/agent-control/results/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Test 5: latest_reviewer_record mismatch
run_negative_test "latest_reviewer_record mismatch" "
    sed -i.bak 's/latest_reviewer_record: task-001-review-12/latest_reviewer_record: task-001-review-11/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 6: owner_acceptance mismatch
run_negative_test "owner_acceptance mismatch" "
    sed -i.bak 's/owner_acceptance: pending/owner_acceptance: accepted/' \
        '$REPO_ROOT/state/CURRENT_STATE.yaml'
"

# Test 7: lifecycle_status mismatch
run_negative_test "lifecycle_status mismatch" "
    python3 -c \"
import json
with open('$REPO_ROOT/agent-control/results/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['lifecycle_status'] = 'complete'
with open('$REPO_ROOT/agent-control/results/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Test 8: formal_closure mismatch
run_negative_test "formal_closure mismatch" "
    sed -i.bak 's/formal_closure: false/formal_closure: true/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 9: task_002_status mismatch
run_negative_test "task_002_status mismatch" "
    python3 -c \"
import json
with open('$REPO_ROOT/agent-control/results/task-001.json') as f:
    data = json.load(f)
data['lifecycle']['task_002_status'] = 'in_progress'
with open('$REPO_ROOT/agent-control/results/task-001.json', 'w') as f:
    json.dump(data, f, indent=2)
\"
"

# Restore originals
cp "$BACKUP_DIR/CURRENT_TASK.yaml" "$REPO_ROOT/agent-control/"
cp "$BACKUP_DIR/CURRENT_STATE.yaml" "$REPO_ROOT/state/"
cp "$BACKUP_DIR/task-001.json" "$REPO_ROOT/agent-control/results/"

# Clean up .bak files
rm -f "$REPO_ROOT/agent-control/CURRENT_TASK.yaml.bak"
rm -f "$REPO_ROOT/state/CURRENT_STATE.yaml.bak"

# Summary
echo ""
echo "=== Negative test summary ==="
echo "Tests run: $test_count"
echo "Tests passed: $pass_count"

if [ "$pass_count" -eq "$test_count" ] && [ "$test_count" -ge 9 ]; then
    echo "✓ All $test_count negative tests passed"
    exit 0
else
    echo "✗ Some tests failed or insufficient coverage (need 9, have $test_count)"
    exit 1
fi
