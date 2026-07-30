#!/usr/bin/env bash
#
# Negative tests for control state consistency checker
#
# Proves the production checker rejects:
# - Stale 'changes_requested' task status
# - Owner acceptance marked 'accepted' without authorization
# - formal_closure: true
# - Task 002 started
# - Mismatch between current state and result records
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

# Test 1: Stale 'changes_requested' status
run_negative_test "stale changes_requested status" "
    sed -i.bak 's/^task_id: task-001-control-plane-repair$/task_id: task-001-core-research/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
    sed -i.bak 's/^status: awaiting_owner_decision$/status: changes_requested/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 2: Owner acceptance marked 'accepted' without authorization
run_negative_test "owner acceptance accepted without auth" "
    sed -i.bak 's/owner_acceptance: pending/owner_acceptance: accepted/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 3: formal_closure true
run_negative_test "formal closure true" "
    sed -i.bak 's/formal_closure: false/formal_closure: true/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 4: Task 002 started
run_negative_test "task 002 started" "
    sed -i.bak 's/task_002_status: not_started/task_002_status: in_progress/' \
        '$REPO_ROOT/agent-control/CURRENT_TASK.yaml'
"

# Test 5: Mismatch between state and result
run_negative_test "state/result mismatch" "
    sed -i.bak 's/owner_acceptance: pending/owner_acceptance: accepted/' \
        '$REPO_ROOT/state/CURRENT_STATE.yaml'
"

# Restore originals
cp "$BACKUP_DIR/CURRENT_TASK.yaml" "$REPO_ROOT/agent-control/"
cp "$BACKUP_DIR/CURRENT_STATE.yaml" "$REPO_ROOT/state/"
cp "$BACKUP_DIR/task-001.json" "$REPO_ROOT/agent-control/results/"

# Summary
echo ""
echo "=== Negative test summary ==="
echo "Tests run: $test_count"
echo "Tests passed: $pass_count"

if [ "$pass_count" -eq "$test_count" ]; then
    echo "✓ All negative tests passed"
    exit 0
else
    echo "✗ Some tests failed"
    exit 1
fi
