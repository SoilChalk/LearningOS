#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CHECKER="$SCRIPT_DIR/check_control_state.py"
TASK_FILE="$REPO_ROOT/agent-control/CURRENT_TASK.yaml"
STATE_FILE="$REPO_ROOT/state/CURRENT_STATE.yaml"
RESULT_REL=$(awk -F': ' '/^result_file:/ {print $2; exit}' "$TASK_FILE")
RESULT_FILE="$REPO_ROOT/$RESULT_REL"

FIXTURE_DIR=$(mktemp -d)
trap 'rm -rf "$FIXTURE_DIR"' EXIT

copy_fixtures() {
  cp "$TASK_FILE" "$FIXTURE_DIR/CURRENT_TASK.yaml"
  cp "$STATE_FILE" "$FIXTURE_DIR/CURRENT_STATE.yaml"
  cp "$RESULT_FILE" "$FIXTURE_DIR/task-result.json"
}

run_checker() {
  python3 "$CHECKER" \
    --current-task "$FIXTURE_DIR/CURRENT_TASK.yaml" \
    --current-state "$FIXTURE_DIR/CURRENT_STATE.yaml" \
    --task-result "$FIXTURE_DIR/task-result.json"
}

HASH_TASK_BEFORE=$(shasum -a 256 "$TASK_FILE" | awk '{print $1}')
HASH_STATE_BEFORE=$(shasum -a 256 "$STATE_FILE" | awk '{print $1}')
HASH_RESULT_BEFORE=$(shasum -a 256 "$RESULT_FILE" | awk '{print $1}')

count=0
passed=0

positive() {
  count=$((count + 1))
  copy_fixtures
  if run_checker >/dev/null 2>&1; then
    echo "✓ Test $count: valid active task passes"
    passed=$((passed + 1))
  else
    echo "✗ Test $count: valid active task rejected"
    exit 1
  fi
}

negative() {
  local name="$1"
  local mutation="$2"
  count=$((count + 1))
  copy_fixtures
  eval "$mutation"
  if run_checker >/dev/null 2>&1; then
    echo "✗ Test $count: $name was not rejected"
    exit 1
  else
    echo "✓ Test $count: $name rejected"
    passed=$((passed + 1))
  fi
}

positive

negative "state status mismatch" "sed -i.bak 's/^status: ready$/status: in_progress/' '$FIXTURE_DIR/CURRENT_STATE.yaml'; rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'"

negative "result task_id mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['task_id']='wrong-task'
json.dump(d, open(p,'w'), indent=2)
PY"

negative "previous_agent_execution mismatch" "sed -i.bak 's/previous_agent_execution: not_started/previous_agent_execution: interrupted/' '$FIXTURE_DIR/CURRENT_STATE.yaml'; rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'"

negative "technical_completion mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['lifecycle']['technical_completion']='candidate_complete'
json.dump(d, open(p,'w'), indent=2)
PY"

negative "reviewer_acceptance mismatch" "sed -i.bak 's/reviewer_acceptance: pending/reviewer_acceptance: accepted/' '$FIXTURE_DIR/CURRENT_TASK.yaml'; rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'"

negative "latest_reviewer_record mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['lifecycle']['latest_reviewer_record']='unexpected-review'
json.dump(d, open(p,'w'), indent=2)
PY"

negative "owner_acceptance mismatch" "sed -i.bak 's/owner_acceptance: authorized/owner_acceptance: pending/' '$FIXTURE_DIR/CURRENT_STATE.yaml'; rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'"

negative "lifecycle_status mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['lifecycle']['lifecycle_status']='in_progress'
json.dump(d, open(p,'w'), indent=2)
PY"

negative "formal_closure mismatch" "sed -i.bak 's/formal_closure: false/formal_closure: true/' '$FIXTURE_DIR/CURRENT_TASK.yaml'; rm -f '$FIXTURE_DIR/CURRENT_TASK.yaml.bak'"

negative "task_002_status mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['lifecycle']['task_002_status']='in_progress'
json.dump(d, open(p,'w'), indent=2)
PY"

HASH_TASK_AFTER=$(shasum -a 256 "$TASK_FILE" | awk '{print $1}')
HASH_STATE_AFTER=$(shasum -a 256 "$STATE_FILE" | awk '{print $1}')
HASH_RESULT_AFTER=$(shasum -a 256 "$RESULT_FILE" | awk '{print $1}')

if [[ "$HASH_TASK_BEFORE" != "$HASH_TASK_AFTER" || "$HASH_STATE_BEFORE" != "$HASH_STATE_AFTER" || "$HASH_RESULT_BEFORE" != "$HASH_RESULT_AFTER" ]]; then
  echo "✗ Live authority files changed during fixture tests"
  exit 1
fi

echo "✓ Live authority files unchanged"
echo "✓ $passed/$count tests passed"
test "$passed" -eq 11
