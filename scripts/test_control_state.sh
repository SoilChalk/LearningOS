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

negative "state status mismatch" "sed -i.bak -E 's/^status: .*/status: in_progress/' '$FIXTURE_DIR/CURRENT_STATE.yaml'; rm -f '$FIXTURE_DIR/CURRENT_STATE.yaml.bak'"

negative "result task_id mismatch" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d['task_id']='wrong-task'
json.dump(d, open(p,'w'), indent=2)
PY"

negative "result missing status" "python3 - <<'PY'
import json
p='$FIXTURE_DIR/task-result.json'
d=json.load(open(p))
d.pop('status', None)
json.dump(d, open(p,'w'), indent=2)
PY"

count=$((count + 1))
copy_fixtures
sed -i.bak '/^result_file:/d' "$FIXTURE_DIR/CURRENT_TASK.yaml"
rm -f "$FIXTURE_DIR/CURRENT_TASK.yaml.bak"
if python3 "$CHECKER" --current-task "$FIXTURE_DIR/CURRENT_TASK.yaml" --current-state "$FIXTURE_DIR/CURRENT_STATE.yaml" >/dev/null 2>&1; then
  echo "✗ Test $count: contract missing result_file was not rejected"
  exit 1
else
  echo "✓ Test $count: contract missing result_file rejected"
  passed=$((passed + 1))
fi

negative "result file malformed" "echo 'not json' > '$FIXTURE_DIR/task-result.json'"

HASH_TASK_AFTER=$(shasum -a 256 "$TASK_FILE" | awk '{print $1}')
HASH_STATE_AFTER=$(shasum -a 256 "$STATE_FILE" | awk '{print $1}')
HASH_RESULT_AFTER=$(shasum -a 256 "$RESULT_FILE" | awk '{print $1}')

if [[ "$HASH_TASK_BEFORE" != "$HASH_TASK_AFTER" || "$HASH_STATE_BEFORE" != "$HASH_STATE_AFTER" || "$HASH_RESULT_BEFORE" != "$HASH_RESULT_AFTER" ]]; then
  echo "✗ Live authority files changed during fixture tests"
  exit 1
fi

echo "✓ Live authority files unchanged"
echo "✓ $passed/$count tests passed"
test "$passed" -eq 6
