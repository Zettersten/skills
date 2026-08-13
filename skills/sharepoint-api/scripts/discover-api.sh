#!/usr/bin/env bash
set -euo pipefail

# discover-api.sh - Discover SharePoint API endpoints via HAR capture
#
# Captures network traffic while navigating SharePoint UI to discover API endpoints.

SESSION="${AGENT_BROWSER_SESSION:-}"
OUTPUT_FILE="${1:-/tmp/sharepoint-apis.har}"

usage() {
  cat <<EOF
Usage: $0 [output-file]

Capture network traffic to discover SharePoint API endpoints.

Arguments:
  output-file          HAR file path (default: /tmp/sharepoint-apis.har)

Environment Variables:
  AGENT_BROWSER_SESSION Current session ID (required)

Example:
  bash $0 /tmp/capture.har
EOF
}

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
  usage
  exit 0
fi

if [[ -z "$SESSION" ]]; then
  echo "Error: AGENT_BROWSER_SESSION not set" >&2
  echo "Create session first: bash scripts/session-manager.sh create" >&2
  exit 1
fi

echo "Starting HAR capture..."
echo "Output: $OUTPUT_FILE"
echo ""

agent-browser --session "$SESSION" network har start

echo "Navigate SharePoint UI now (browse folders, search, etc.)"
echo ""
echo "Press Enter when done..."
read -r

echo ""
echo "Stopping capture..."
agent-browser --session "$SESSION" network har stop "$OUTPUT_FILE"

echo ""
echo "Analyzing captured APIs..."
echo ""

if command -v jq >/dev/null 2>&1; then
  jq '.log.entries[] | select(.request.url | contains("_api")) | {
    method: .request.method,
    url: .request.url,
    status: .response.status
  }' "$OUTPUT_FILE" | jq -s 'unique_by(.url)' | jq -r '.[] | "\(.method) \(.url) (\(.status))"'
else
  echo "Install jq to analyze HAR: brew install jq"
fi

echo ""
echo "✓ HAR file saved: $OUTPUT_FILE"
echo ""
echo "Analyze with:"
echo "  jq '.log.entries[] | select(.request.url | contains(\"_api\"))' $OUTPUT_FILE"
