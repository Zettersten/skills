#!/usr/bin/env bash
set -euo pipefail

# upload-file.sh - Upload files to SharePoint
#
# Uploads files using GetFolderByServerRelativeUrl API.

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/.config"

# Load configuration if exists
if [[ -f "$CONFIG_FILE" ]]; then
  source "$CONFIG_FILE"
fi

# Configuration from environment (can override config file)
SP_TENANT_URL="${SP_TENANT_URL:-}"
SP_USER_PATH="${SP_USER_PATH:-}"
SESSION="${AGENT_BROWSER_SESSION:-}"

# Parameters
LOCAL_FILE=""
REMOTE_PATH=""
OVERWRITE="false"

# Usage
usage() {
  cat <<EOF
Usage: $0 <local-file> <remote-path> [options]

Upload files to SharePoint/OneDrive.

Arguments:
  local-file            Local file path to upload
  remote-path           Remote path (folder or full path with filename)

Options:
  --overwrite           Overwrite if file exists (default: fail on conflict)
  -h, --help           Show this help message

Environment Variables:
  SP_TENANT_URL         SharePoint tenant base URL (required)
  SP_USER_PATH          Personal site path (required)
  AGENT_BROWSER_SESSION Current session ID (required)

Examples:
  # Upload to folder
  bash $0 local.pdf "Documents/"

  # Upload with new name
  bash $0 local.pdf "Documents/remote.pdf"

  # Overwrite existing
  bash $0 file.pdf "Documents/file.pdf" --overwrite
EOF
}

# Parse arguments
if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

LOCAL_FILE="$1"
REMOTE_PATH="$2"
shift 2

while [[ $# -gt 0 ]]; do
  case "$1" in
    --overwrite)
      OVERWRITE="true"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

# Validate
if [[ ! -f "$LOCAL_FILE" ]]; then
  echo "Error: File not found: $LOCAL_FILE" >&2
  exit 1
fi

if [[ -z "$SP_TENANT_URL" ]] || [[ -z "$SESSION" ]]; then
  echo "Error: Missing SP_TENANT_URL or AGENT_BROWSER_SESSION" >&2
  exit 1
fi

# Determine folder and filename
if [[ "$REMOTE_PATH" == */ ]]; then
  # Path ends with / -> folder
  FOLDER="$REMOTE_PATH"
  FILENAME=$(basename "$LOCAL_FILE")
else
  # Full path with filename
  FOLDER=$(dirname "$REMOTE_PATH")/
  FILENAME=$(basename "$REMOTE_PATH")
fi

echo "Uploading: $LOCAL_FILE"
echo "To: ${FOLDER}${FILENAME}"
echo "Overwrite: $OVERWRITE"
echo ""

# Read file as base64
FILE_CONTENT=$(base64 < "$LOCAL_FILE")

# Export for JavaScript
export SP_TENANT_URL
export FOLDER
export FILENAME
export FILE_CONTENT
export OVERWRITE

# Upload via API
RESULT=$(cat <<'EOF' | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const SP_TENANT_URL = process.env.SP_TENANT_URL;
  const FOLDER = process.env.FOLDER;
  const FILENAME = process.env.FILENAME;
  const FILE_CONTENT = process.env.FILE_CONTENT;
  const OVERWRITE = process.env.OVERWRITE === 'true';

  // Decode base64
  const binaryString = atob(FILE_CONTENT);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  // Upload
  const uploadUrl = `${SP_TENANT_URL}/_api/web/GetFolderByServerRelativeUrl('${FOLDER}')/Files/add(url='${FILENAME}',overwrite=${OVERWRITE})`;

  try {
    const response = await fetch(uploadUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/octet-stream'
      },
      body: bytes.buffer
    });

    if (!response.ok) {
      return JSON.stringify({ error: true, status: response.status });
    }

    const data = await response.json();
    return JSON.stringify({ success: true, file: data.d }, null, 2);
  } catch (error) {
    return JSON.stringify({ error: true, message: error.message });
  }
})();
EOF
)

if echo "$RESULT" | jq -e '.error' >/dev/null 2>&1; then
  echo "Error: Upload failed" >&2
  echo "$RESULT" | jq '.' >&2
  exit 1
fi

echo "✓ Upload complete"
echo "$RESULT" | jq '.file.Name, .file.ServerRelativeUrl'
