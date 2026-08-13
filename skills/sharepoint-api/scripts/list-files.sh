#!/usr/bin/env bash
set -euo pipefail

# list-files.sh - List and filter SharePoint files
#
# Lists files using SharePoint RenderListDataAsStream API with
# support for filtering, pagination, and multiple output formats.

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
SP_RENDER_OPTIONS="${SP_RENDER_OPTIONS:-5691143}"
SESSION="${AGENT_BROWSER_SESSION:-}"

# Parameters
FOLDER=""
FILE_TYPE=""
LIMIT=""
FORMAT="json"
MODIFIED_AFTER=""
MODIFIED_BEFORE=""

# Usage
usage() {
  cat <<EOF
Usage: $0 [options]

List and filter SharePoint/OneDrive files using RenderListDataAsStream API.

Options:
  --folder <path>         List files in subfolder (e.g., "Projects/2024")
  --type <ext>            Filter by file type (e.g., docx, pptx, xlsx)
  --limit <num>           Limit number of results
  --format <fmt>          Output format: json, csv, table (default: json)
  --modified-after <date> Filter files modified after date (ISO format)
  --modified-before <date> Filter files modified before date (ISO format)
  -h, --help             Show this help message

Environment Variables:
  SP_TENANT_URL         SharePoint tenant base URL (required)
  SP_USER_PATH          Personal site path (required)
  SP_RENDER_OPTIONS     RenderListDataAsStream options (default: 5691143)
  AGENT_BROWSER_SESSION Current session ID (required)

Examples:
  # List root files
  bash $0

  # List subfolder
  bash $0 --folder "Projects/2024"

  # Filter by type
  bash $0 --type pptx --limit 10

  # CSV output
  bash $0 --format csv

  # Date filter
  bash $0 --modified-after "2024-01-01" --format table
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --folder=*)
      FOLDER="${1#--folder=}"
      ;;
    --folder)
      FOLDER="$2"
      shift
      ;;
    --type=*)
      FILE_TYPE="${1#--type=}"
      ;;
    --type)
      FILE_TYPE="$2"
      shift
      ;;
    --limit=*)
      LIMIT="${1#--limit=}"
      ;;
    --limit)
      LIMIT="$2"
      shift
      ;;
    --format=*)
      FORMAT="${1#--format=}"
      ;;
    --format)
      FORMAT="$2"
      shift
      ;;
    --modified-after=*)
      MODIFIED_AFTER="${1#--modified-after=}"
      ;;
    --modified-after)
      MODIFIED_AFTER="$2"
      shift
      ;;
    --modified-before=*)
      MODIFIED_BEFORE="${1#--modified-before=}"
      ;;
    --modified-before)
      MODIFIED_BEFORE="$2"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'" >&2
      echo "" >&2
      usage
      exit 1
      ;;
  esac
  shift
done

# Validate configuration
if [[ -z "$SP_TENANT_URL" ]]; then
  echo "Error: SP_TENANT_URL not set" >&2
  exit 1
fi

if [[ -z "$SP_USER_PATH" ]]; then
  echo "Error: SP_USER_PATH not set" >&2
  exit 1
fi

if [[ -z "$SESSION" ]]; then
  echo "Error: AGENT_BROWSER_SESSION not set" >&2
  echo "Create a session with: bash scripts/session-manager.sh create" >&2
  exit 1
fi

# Validate format
if [[ ! "$FORMAT" =~ ^(json|csv|table)$ ]]; then
  echo "Error: Invalid format '$FORMAT'. Must be: json, csv, table" >&2
  exit 1
fi

# Build ViewXml for filtering
build_viewxml() {
  local view_xml="<View>"
  local has_query=false

  # Build query if filters present
  if [[ -n "$FILE_TYPE" ]] || [[ -n "$MODIFIED_AFTER" ]] || [[ -n "$MODIFIED_BEFORE" ]]; then
    view_xml+="<Query><Where>"
    has_query=true

    # Multiple conditions -> use <And>
    local conditions=()

    if [[ -n "$FILE_TYPE" ]]; then
      conditions+=("<Eq><FieldRef Name=\"File_x0020_Type\"/><Value Type=\"Text\">$FILE_TYPE</Value></Eq>")
    fi

    if [[ -n "$MODIFIED_AFTER" ]]; then
      conditions+=("<Geq><FieldRef Name=\"Modified\"/><Value Type=\"DateTime\">$MODIFIED_AFTER</Value></Geq>")
    fi

    if [[ -n "$MODIFIED_BEFORE" ]]; then
      conditions+=("<Leq><FieldRef Name=\"Modified\"/><Value Type=\"DateTime\">$MODIFIED_BEFORE</Value></Leq>")
    fi

    # Wrap multiple conditions in <And>
    if [[ ${#conditions[@]} -eq 1 ]]; then
      view_xml+="${conditions[0]}"
    elif [[ ${#conditions[@]} -eq 2 ]]; then
      view_xml+="<And>${conditions[0]}${conditions[1]}</And>"
    elif [[ ${#conditions[@]} -eq 3 ]]; then
      view_xml+="<And><And>${conditions[0]}${conditions[1]}</And>${conditions[2]}</And>"
    fi

    view_xml+="</Where></Query>"
  fi

  # Add row limit
  if [[ -n "$LIMIT" ]]; then
    view_xml+="<RowLimit>$LIMIT</RowLimit>"
  fi

  view_xml+="</View>"

  echo "$view_xml"
}

VIEW_XML=$(build_viewxml)

# Strip trailing slash from tenant URL
SP_TENANT_URL="${SP_TENANT_URL%/}"

# Execute API call via agent-browser
# Note: Using heredoc without quotes (<<EOF not <<'EOF') to enable bash variable substitution
RESULT=$(cat <<EOF | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const SP_TENANT_URL = "$SP_TENANT_URL";
  const SP_USER_PATH = "$SP_USER_PATH";
  const SP_RENDER_OPTIONS = parseInt("$SP_RENDER_OPTIONS");
  const FOLDER = "$FOLDER";
  const VIEW_XML = \`$VIEW_XML\`;

  // Build endpoint URL
  const documentsPath = SP_USER_PATH + '/Documents' + (FOLDER ? '/' + FOLDER : '');
  const encodedPath = encodeURIComponent(documentsPath);
  const url = \`\${SP_TENANT_URL}\${SP_USER_PATH}/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1='\${encodedPath}'&TryNewExperienceSingle=TRUE\`;

  // Build request parameters
  const params = {
    __metadata: { type: 'SP.RenderListDataParameters' },
    RenderOptions: SP_RENDER_OPTIONS
  };

  // Add folder parameter if specified
  if (FOLDER) {
    params.FolderServerRelativeUrl = documentsPath;
  }

  // Add ViewXml if filters present
  if (VIEW_XML && VIEW_XML !== '<View></View>') {
    params.ViewXml = VIEW_XML;
  }

  try {
    // Make API call
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json;odata=verbose',
        'Content-Type': 'application/json;odata=verbose'
      },
      body: JSON.stringify({ parameters: params })
    });

    if (!response.ok) {
      return JSON.stringify({
        error: true,
        status: response.status,
        statusText: response.statusText
      }, null, 2);
    }

    const data = await response.json();

    // Map response to simplified format
    const files = data.ListData.Row.map(item => ({
      name: item.FileLeafRef,
      type: item.FSObjType === '1' ? 'folder' : 'file',
      size: parseInt(item.SMTotalSize || 0),
      modified: item['Modified.'],
      fileType: item['File_x0020_Type'] || 'folder',
      path: item.FileRef
    }));

    return JSON.stringify(files, null, 2);
  } catch (error) {
    return JSON.stringify({
      error: true,
      message: error.message
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

# Format output
case "$FORMAT" in
  json)
    echo "$RESULT" | jq '.'
    ;;
  csv)
    echo "name,type,size,modified,fileType,path"
    echo "$RESULT" | jq -r '.[] | [.name, .type, .size, .modified, .fileType, .path] | @csv'
    ;;
  table)
    echo "$RESULT" | jq -r '["NAME", "TYPE", "SIZE", "MODIFIED", "FILE_TYPE", "PATH"], (.[] | [.name, .type, .size, .modified, .fileType, .path]) | @tsv' | column -t -s $'\t'
    ;;
esac
