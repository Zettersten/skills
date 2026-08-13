#!/usr/bin/env bash
set -euo pipefail

# list-files-graph.sh - List files using Microsoft Graph API
#
# More reliable than SharePoint REST API. Uses /_api/v2.0/me/drive endpoints.

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/.config"

# Load configuration if exists
if [[ -f "$CONFIG_FILE" ]]; then
  source "$CONFIG_FILE"
fi

# Configuration
SP_TENANT_URL="${SP_TENANT_URL:-}"
SESSION="${AGENT_BROWSER_SESSION:-}"
FOLDER="${1:-}"  # Optional folder path

# Validate required variables
if [[ -z "$SP_TENANT_URL" ]]; then
  echo "Error: SP_TENANT_URL not set" >&2
  exit 1
fi

if [[ -z "$SESSION" ]]; then
  echo "Error: AGENT_BROWSER_SESSION not set" >&2
  echo "Create a session with: bash scripts/session-manager.sh create" >&2
  exit 1
fi

# Strip trailing slash
SP_TENANT_URL="${SP_TENANT_URL%/}"

# Build Graph API path
if [[ -n "$FOLDER" ]]; then
  # List specific folder
  GRAPH_PATH="/drive/root:/$FOLDER:/children"
else
  # List root
  GRAPH_PATH="/drive/root/children"
fi

# Execute API call
RESULT=$(cat <<EOF | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const url = "$SP_TENANT_URL/_api/v2.0/me$GRAPH_PATH";

  try {
    const response = await fetch(url);
    if (!response.ok) {
      return JSON.stringify({
        error: true,
        status: response.status,
        statusText: response.statusText,
        url: url
      }, null, 2);
    }

    const data = await response.json();

    // Map to consistent format
    const files = data.value.map(item => ({
      name: item.name,
      type: item.folder ? 'folder' : 'file',
      size: item.size,
      modified: item.lastModifiedDateTime,
      fileType: item.file ? item.file.fileExtension : 'folder',
      webUrl: item.webUrl,
      downloadUrl: item['@microsoft.graph.downloadUrl'] || item['@content.downloadUrl'] || null
    }));

    return JSON.stringify(files, null, 2);
  } catch (error) {
    return JSON.stringify({
      error: true,
      message: error.message,
      stack: error.stack
    }, null, 2);
  }
})();
EOF
)

# Check for errors
if echo "$RESULT" | jq -e '.error' >/dev/null 2>&1; then
  echo "Error: API call failed" >&2
  echo "$RESULT" | jq '.' >&2
  exit 1
fi

# Output as JSON
echo "$RESULT" | jq '.'
