#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/log_optimized.txt"
TIME_FILE="$SCRIPT_DIR/time_optimized.txt"

if [ -d "$SCRIPT_DIR/.venv" ]; then
  # shellcheck source=/dev/null
  source "$SCRIPT_DIR/.venv/bin/activate"
fi

START=$(python - <<'PY'
import time
print(time.perf_counter())
PY
)

set +e
pytest "$SCRIPT_DIR/test_optimized.py" --disable-warnings -q | tee "$LOG_FILE"
STATUS=${PIPESTATUS[0]}
set -e

END=$(python - <<'PY'
import time
print(time.perf_counter())
PY
)

ELAPSED=$(python - <<PY
start = float("$START")
end = float("$END")
print(f"{end - start:.6f}")
PY
)

{
  echo "status=$STATUS"
  echo "elapsed_seconds=$ELAPSED"
  echo "timestamp=$(date --iso-8601=seconds 2>/dev/null || date)"
} > "$TIME_FILE"

exit "$STATUS"
