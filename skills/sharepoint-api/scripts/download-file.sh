#!/usr/bin/env bash
set -euo pipefail

# download-file.sh - Download files from SharePoint
#
# Downloads files using direct FileRef paths with browser authentication.

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
FILE_PATH=""
OUTPUT_DIR="."
FORCE_DOWNLOAD="true"

# Usage
usage() {
  cat <<EOF
Usage: $0 <file-path> [options]

Download files from SharePoint/OneDrive using direct paths.

Arguments:
  file-path              Relative path to file (e.g., "Documents/report.pdf")

Options:
  --output <dir>         Output directory (default: current directory)
  --no-force-download    Don't force download (allow preview)
  -h, --help            Show this help message

Environment Variables:
  SP_TENANT_URL         SharePoint tenant base URL (required)
  SP_USER_PATH          Personal site path (required)
  AGENT_BROWSER_SESSION Current session ID (required)

Examples:
  # Download to current directory
  bash $0 "Documents/report.pdf"

  # Download to specific directory
  bash $0 "Documents/report.pdf" --output ~/Downloads/

  # Allow preview (no forced download)
  bash $0 "Documents/image.png" --no-force-download
EOF
}

# Parse arguments
if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

FILE_PATH="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output=*)
      OUTPUT_DIR="${1#--output=}"
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift
      ;;
    --no-force-download)
      FORCE_DOWNLOAD="false"
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

# Validate configuration
if [[ -z "$SP_TENANT_URL" ]] || [[ -z "$SP_USER_PATH" ]] || [[ -z "$SESSION" ]]; then
  echo "Error: Missing required configuration" >&2
  echo "Set SP_TENANT_URL, SP_USER_PATH, and AGENT_BROWSER_SESSION" >&2
  exit 1
fi

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Build download URL
FILE_URL="${SP_TENANT_URL}${SP_USER_PATH}/${FILE_PATH}"
if [[ "$FORCE_DOWNLOAD" == "true" ]]; then
  FILE_URL="${FILE_URL}?download=1"
fi

# Get filename
FILENAME=$(basename "$FILE_PATH")
OUTPUT_FILE="$OUTPUT_DIR/$FILENAME"

echo "Downloading: $FILE_PATH"
echo "From: $FILE_URL"
echo "To: $OUTPUT_FILE"
echo ""

# Check file exists and get metadata
METADATA=$(cat <<EOF | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const response = await fetch("$FILE_URL", { method: 'HEAD' });
  if (!response.ok) {
    return JSON.stringify({ error: true, status: response.status });
  }
  return JSON.stringify({
    ok: true,
    contentType: response.headers.get('content-type'),
    contentLength: response.headers.get('content-length')
  });
})();
EOF
)

if echo "$METADATA" | jq -e '.error' >/dev/null 2>&1; then
  STATUS=$(echo "$METADATA" | jq -r '.status')
  echo "Error: File not found (HTTP $STATUS)" >&2
  exit 1
fi

CONTENT_TYPE=$(echo "$METADATA" | jq -r '.contentType')
CONTENT_LENGTH=$(echo "$METADATA" | jq -r '.contentLength')

echo "Content-Type: $CONTENT_TYPE"
echo "Content-Length: $CONTENT_LENGTH bytes"
echo ""

# Download file
echo "Downloading..."

# Note: Using agent-browser screenshot/network features would be better for binary files
# This approach converts to base64 for text-based transfer

cat <<EOF | agent-browser --session "$SESSION" eval --stdin > /tmp/download_b64.txt
(async () => {
  const response = await fetch("$FILE_URL");
  const blob = await response.blob();
  const arrayBuffer = await blob.arrayBuffer();
  const uint8Array = new Uint8Array(arrayBuffer);
  // Convert to base64 using browser APIs (not Node.js Buffer)
  let binary = '';
  uint8Array.forEach(byte => binary += String.fromCharCode(byte));
  return btoa(binary);
})();
EOF

# Decode base64 to file
base64 -d /tmp/download_b64.txt > "$OUTPUT_FILE"
rm -f /tmp/download_b64.txt

# Decode base64 to file
if command -v base64 >/dev/null 2>&1; then
  base64 -d -i "$OUTPUT_FILE" -o "$OUTPUT_FILE.tmp" 2>/dev/null || {
    echo "Warning: base64 decode method 1 failed, trying alternative..." >&2
    cat "$OUTPUT_FILE" | base64 -d > "$OUTPUT_FILE.tmp"
  }
  mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"
fi

echo "✓ Downloaded: $OUTPUT_FILE"
ls -lh "$OUTPUT_FILE"
