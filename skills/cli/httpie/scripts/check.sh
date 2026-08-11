#!/usr/bin/env bash
# check.sh — Test an HTTP endpoint using httpie
#
# Useful for:
#   - Verifying an API is reachable and returns the expected status
#   - Timing responses to detect slowness
#   - Watching an endpoint during deploys or restarts
#   - Asserting a specific field in a JSON response
#
# Usage:
#   bash check.sh <url>                          Expect 200, print result
#   bash check.sh <url> --expect=201            Expect a specific status code
#   bash check.sh <url> --method=POST           Use a different HTTP method
#   bash check.sh <url> --auth="Bearer TOKEN"   Add Authorization header
#   bash check.sh <url> --json-key=.status      Assert a jq path in the response body
#   bash check.sh <url> --json-val=ok           Expected value for --json-key assertion
#   bash check.sh <url> --watch[=SECS]          Repeat every N seconds (default: 5)
#   bash check.sh <url> --quiet                 Exit 0/1 only, no output (CI/scripts)
#   bash check.sh <url> --verbose               Also print response headers and body
#
# Examples:
#   bash check.sh https://api.example.com/health
#   bash check.sh https://api.example.com/health --watch
#   bash check.sh https://api.example.com/users --method=POST --expect=201
#   bash check.sh https://api.example.com/status --json-key=.status --json-val=ok
#   bash check.sh https://api.example.com/admin --auth="Bearer $TOKEN" --expect=200

set -euo pipefail

# ── Args ──────────────────────────────────────────────────────────────────────

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: $0 <url> [options]" >&2
  echo "  --expect=STATUS   Expected HTTP status code (default: 200)" >&2
  echo "  --method=METHOD   HTTP method (default: GET)" >&2
  echo "  --auth=VALUE      Authorization header value (e.g. 'Bearer TOKEN')" >&2
  echo "  --json-key=PATH   jq path to assert in response JSON (e.g. .status)" >&2
  echo "  --json-val=VALUE  Expected value for json-key (string comparison)" >&2
  echo "  --watch[=SECS]    Poll interval in seconds (default 5)" >&2
  echo "  --quiet           Silent mode: exit 0 = pass, exit 1 = fail" >&2
  echo "  --verbose         Print response headers and body" >&2
  exit 1
fi
shift

EXPECT="200"
METHOD="GET"
AUTH=""
JSON_KEY=""
JSON_VAL=""
WATCH_SECS=0
QUIET=0
VERBOSE=0

for arg in "$@"; do
  case "$arg" in
    --expect=*)   EXPECT="${arg#--expect=}" ;;
    --method=*)   METHOD="${arg#--method=}" ;;
    --auth=*)     AUTH="${arg#--auth=}" ;;
    --json-key=*) JSON_KEY="${arg#--json-key=}" ;;
    --json-val=*) JSON_VAL="${arg#--json-val=}" ;;
    --watch)      WATCH_SECS=5 ;;
    --watch=*)    WATCH_SECS="${arg#--watch=}" ;;
    --quiet)      QUIET=1 ;;
    --verbose)    VERBOSE=1 ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

# ── Helpers ───────────────────────────────────────────────────────────────────

GREEN='\033[32m'; RED='\033[31m'; YELLOW='\033[33m'; DIM='\033[2m'; RESET='\033[0m'
# Disable color when not a tty
[[ -t 1 ]] || { GREEN=''; RED=''; YELLOW=''; DIM=''; RESET=''; }

pass() { [[ "$QUIET" -eq 0 ]] && printf "${GREEN}✓${RESET}  %s\n" "$*" || true; }
fail() { [[ "$QUIET" -eq 0 ]] && printf "${RED}✗${RESET}  %s\n" "$*" >&2 || true; }
info() { [[ "$QUIET" -eq 0 ]] && printf "${DIM}   %s${RESET}\n" "$*" || true; }

# Portable millisecond timer
now_ms() {
  if date +%s%3N &>/dev/null 2>&1; then
    date +%s%3N
  else
    # macOS fallback: python3 for sub-second timing
    python3 -c "import time; print(int(time.time() * 1000))" 2>/dev/null || echo 0
  fi
}

# ── Core check ───────────────────────────────────────────────────────────────

run_check() {
  local http_args=("--follow" "--print=hb")

  [[ -n "$AUTH" ]] && http_args+=("Authorization:$AUTH")

  local t0 t1 elapsed_ms
  t0=$(now_ms)
  RESPONSE=$(http "${http_args[@]}" "$METHOD" "$URL" 2>&1) || true
  t1=$(now_ms)
  elapsed_ms=$(( t1 - t0 ))

  # Parse status from response headers (first HTTP/ line)
  STATUS=$(echo "$RESPONSE" | grep -i '^HTTP/' | tail -1 | awk '{print $2}' || echo "???")

  # Separate headers from body for JSON assertions
  BODY=$(echo "$RESPONSE" | awk '/^\r?$/{found=1; next} found{print}')

  local ok=1
  local notes=()

  # Status check
  if [[ "$STATUS" == "$EXPECT" ]]; then
    notes+=("status ${STATUS}")
  else
    ok=0
    notes+=("status ${STATUS} (expected ${EXPECT})")
  fi

  # JSON key assertion
  if [[ -n "$JSON_KEY" ]]; then
    if ! command -v jq &>/dev/null; then
      notes+=("json-key skipped (jq not installed)")
    else
      ACTUAL=$(echo "$BODY" | jq -r "$JSON_KEY" 2>/dev/null || echo "<parse error>")
      if [[ -n "$JSON_VAL" ]]; then
        if [[ "$ACTUAL" == "$JSON_VAL" ]]; then
          notes+=("${JSON_KEY}=${ACTUAL}")
        else
          ok=0
          notes+=("${JSON_KEY}=${ACTUAL} (expected ${JSON_VAL})")
        fi
      else
        notes+=("${JSON_KEY}=${ACTUAL}")
      fi
    fi
  fi

  # Timing label
  local timing
  if   (( elapsed_ms < 200 ));  then timing="${GREEN}${elapsed_ms}ms${RESET}"
  elif (( elapsed_ms < 1000 )); then timing="${YELLOW}${elapsed_ms}ms${RESET}"
  else                               timing="${RED}${elapsed_ms}ms${RESET}"
  fi

  local note_str
  note_str=$(IFS=', '; echo "${notes[*]}")

  if [[ "$ok" -eq 1 ]]; then
    pass "${URL}  ${timing}  ${DIM}${note_str}${RESET}"
  else
    fail "${URL}  ${elapsed_ms}ms  ${note_str}"
  fi

  if [[ "$VERBOSE" -eq 1 ]]; then
    echo "$RESPONSE" | head -40
  fi

  return $(( 1 - ok ))
}

# ── Run ───────────────────────────────────────────────────────────────────────

if [[ "$WATCH_SECS" -gt 0 ]]; then
  [[ "$QUIET" -eq 0 ]] && echo "Watching ${URL} every ${WATCH_SECS}s  (Ctrl+C to stop)"
  [[ "$QUIET" -eq 0 ]] && echo ""
  EXIT=0
  while true; do
    [[ "$QUIET" -eq 0 ]] && printf "${DIM}[$(date '+%H:%M:%S')]${RESET} "
    run_check || EXIT=1
    sleep "$WATCH_SECS"
  done
  exit "$EXIT"
else
  run_check
fi
