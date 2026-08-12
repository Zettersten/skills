#!/usr/bin/env bash
# scrape.sh — Fetch a URL with browser-like headers using httpie
#
# The key insight: many servers fingerprint requests and block or degrade
# responses for bare API clients. This script sets the headers a real
# Chrome browser sends, which dramatically improves success rates.
#
# Usage:
#   bash scrape.sh <url>                         Raw HTML to stdout
#   bash scrape.sh <url> --text                  Strip HTML tags, print readable text
#   bash scrape.sh <url> --save                  Save to a file named after the URL
#   bash scrape.sh <url> --save=output.html      Save to a specific file
#   bash scrape.sh <url> --status                Print only the HTTP status code
#   bash scrape.sh <url> --headers               Print only the response headers
#   bash scrape.sh <url> --session=NAME          Reuse cookies from a named httpie session
#   bash scrape.sh <url> --no-verify             Skip SSL certificate verification
#   bash scrape.sh <url> --json                  Request JSON (changes Accept header)
#
# Examples:
#   bash scrape.sh https://example.com
#   bash scrape.sh https://example.com --text | head -50
#   bash scrape.sh https://api.example.com/data --json | jq .
#   bash scrape.sh https://example.com --session=mysite
#   bash scrape.sh https://example.com --save=page.html

set -euo pipefail

# ── Args ──────────────────────────────────────────────────────────────────────

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: $0 <url> [--text] [--save[=FILE]] [--status] [--headers] [--session=NAME] [--no-verify] [--json]" >&2
  exit 1
fi
shift

MODE="html"        # html | text | status | headers
SAVE=""            # empty = stdout, filename = save to file
SESSION=""
NO_VERIFY=0
JSON_MODE=0

for arg in "$@"; do
  case "$arg" in
    --text)         MODE="text" ;;
    --status)       MODE="status" ;;
    --headers)      MODE="headers" ;;
    --save)         SAVE="__auto__" ;;
    --save=*)       SAVE="${arg#--save=}" ;;
    --session=*)    SESSION="${arg#--session=}" ;;
    --no-verify)    NO_VERIFY=1 ;;
    --json)         JSON_MODE=1 ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

# ── Browser-like headers ──────────────────────────────────────────────────────
#
# These mirror what Chrome 125 sends. The User-Agent and Accept headers are
# the most important — omitting them is the #1 reason servers return 403/429
# or serve degraded content to scripts.

if [[ "$JSON_MODE" -eq 1 ]]; then
  ACCEPT_HEADER="Accept:application/json,text/plain,*/*;q=0.8"
else
  ACCEPT_HEADER="Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
fi

BROWSER_HEADERS=(
  "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
  "$ACCEPT_HEADER"
  "Accept-Language:en-US,en;q=0.9"
  "Cache-Control:no-cache"
  "Pragma:no-cache"
)

# ── Build httpie args ─────────────────────────────────────────────────────────

HTTP_ARGS=(--follow)

if [[ "$NO_VERIFY" -eq 1 ]]; then
  HTTP_ARGS+=(--verify=no)
fi

if [[ -n "$SESSION" ]]; then
  HTTP_ARGS+=(--session="$SESSION")
fi

# ── Execute ───────────────────────────────────────────────────────────────────

case "$MODE" in
  status)
    # Print just the numeric status code — useful in scripts/conditions
    http "${HTTP_ARGS[@]}" -h GET "$URL" "${BROWSER_HEADERS[@]}" \
      | grep -i '^HTTP/' | tail -1 | awk '{print $2}'
    exit 0
    ;;

  headers)
    http "${HTTP_ARGS[@]}" -h GET "$URL" "${BROWSER_HEADERS[@]}"
    exit 0
    ;;

  text)
    # Fetch body then strip HTML — good for reading article content or checking
    # visible text without a full headless browser
    http "${HTTP_ARGS[@]}" -b GET "$URL" "${BROWSER_HEADERS[@]}" \
      | sed \
          -e 's/<script[^>]*>.*<\/script>//gI' \
          -e 's/<style[^>]*>.*<\/style>//gI' \
          -e 's/<[^>]*>//g' \
          -e 's/&amp;/\&/g' \
          -e 's/&lt;/</g' \
          -e 's/&gt;/>/g' \
          -e 's/&nbsp;/ /g' \
          -e 's/&#[0-9]*;//g' \
          -e 's/&quot;/"/g' \
      | sed '/^\s*$/d'
    exit 0
    ;;

  html)
    BODY=$(http "${HTTP_ARGS[@]}" -b GET "$URL" "${BROWSER_HEADERS[@]}")

    if [[ -n "$SAVE" ]]; then
      if [[ "$SAVE" == "__auto__" ]]; then
        # Derive a safe filename from the URL
        SAVE="$(echo "$URL" | sed 's|https\?://||; s|[/?&=:#]|_|g; s|_*$||').html"
      fi
      echo "$BODY" > "$SAVE"
      echo "Saved to: $SAVE" >&2
    else
      echo "$BODY"
    fi
    ;;
esac
