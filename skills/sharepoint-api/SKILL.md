---
name: sharepoint-api
description: Automate SharePoint/OneDrive operations using agent-browser and SharePoint REST APIs. List files, download/upload documents, filter with CAML queries, search content, and discover new APIs via HAR capture. Works with Commercial, GCC, and GCC High tenants. Triggers include "list SharePoint files", "download from OneDrive", "upload to SharePoint", "search SharePoint documents", "SharePoint API automation", or "OneDrive for Business operations".
license: MIT
compatibility: Requires agent-browser >= 2.0. Install with `npm install -g agent-browser` or `brew install agent-browser`. Chrome/Chromium required for browser automation.
metadata:
  author: Zettersten
  version: "1.0"
  docs: https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest
---

# SharePoint/OneDrive API Automation

Automate SharePoint and OneDrive for Business operations using agent-browser with SharePoint REST APIs. Execute authenticated API calls from JavaScript within a browser context, avoiding OAuth token management while gaining full access to SharePoint's RenderListDataAsStream, Graph API (SharePoint-hosted), and direct file operations.

## Why This Approach

**API over browser automation** → 10-100x faster, reliable, structured data, composable with jq/other tools.

**agent-browser for authentication** → Inherits session cookies from authenticated browser profile, no OAuth flow required.

**Works across tenant types** → Commercial, GCC, GCC High with URL configuration only.

## ⚠️ Critical: Browser JavaScript Context

**agent-browser executes JavaScript in Chromium browser, NOT Node.js.**

Browser JavaScript does NOT have `process.env`. All scripts use bash template substitution to pass variables.

**✅ Correct Pattern (used throughout skill):**
```bash
VAR="value"
cat <<EOF | agent-browser eval --stdin
const myVar = "$VAR";  // Bash substitutes before sending to browser
EOF
```

**❌ Wrong Pattern (will fail):**
```bash
export VAR="value"
cat <<'EOF' | agent-browser eval --stdin
const myVar = process.env.VAR;  // ERROR: process not defined in browser
EOF
```

**Key differences:**
- Use `<<EOF` (no quotes) to enable bash variable substitution
- Use `<<'EOF'` (with quotes) to prevent substitution
- Escape template literals: `\`\${variable}\`` in heredoc
- Browser has `fetch()`, `window`, `document` 
- Browser lacks `process`, `require()`, `Buffer`, `fs`

## Prerequisites

1. **agent-browser** installed and in PATH
2. **Chrome/Chromium** browser

**Note**: SharePoint profile and configuration are created automatically by the skill on first use via an interactive wizard.

## Quick Start

### 1. Provision Profile (First Time Only)

On first use, the skill will automatically prompt you to provision a SharePoint profile:

```bash
cd /path/to/skills/sharepoint-api

# Create session (will launch provision wizard if needed)
bash scripts/session-manager.sh create
```

The wizard will:
1. Prompt for your tenant type (Commercial, GCC High, or Custom)
2. Collect tenant URL and user path
3. Open a browser for Microsoft 365 authentication
4. Save configuration to `.config` file
5. Store authenticated profile in `profile/` directory

**Or provision explicitly**:

```bash
bash scripts/provision-profile.sh
```

### 2. Create Session

After provisioning, create sessions normally:

```bash
bash scripts/session-manager.sh create
```

Configuration is automatically loaded from `.config` file.

### 3. Use the Skill

```bash
# List root files
bash scripts/list-files.sh

# List subfolder
bash scripts/list-files.sh --folder "Projects/2024"

# Filter by type
bash scripts/list-files.sh --type pptx --limit 10

# Download file
bash scripts/download-file.sh "Documents/report.pdf"
```

All scripts automatically load configuration from `.config` file.

## Core Patterns

### Session Management

The skill automatically manages browser profile locks:

```bash
# Create session (handles cleanup automatically)
bash scripts/session-manager.sh create

# Check status
bash scripts/session-manager.sh status

# Cleanup manually if needed
bash scripts/session-manager.sh cleanup
```

Profile is stored in `<skill-dir>/profile/` and managed by the skill.

### API Call Pattern

Execute JavaScript `fetch()` within authenticated browser context:

```bash
cat <<'EOF' | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const response = await fetch('https://TENANT/_api/ENDPOINT', {
    method: 'POST',
    headers: {
      'Accept': 'application/json;odata=verbose',
      'Content-Type': 'application/json;odata=verbose'
    },
    body: JSON.stringify({ /* parameters */ })
  });
  
  const data = await response.json();
  return JSON.stringify(data, null, 2);
})();
EOF
```

### Error Handling

```bash
# Check response status
cat <<'EOF' | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const response = await fetch(url, options);
  if (!response.ok) {
    return JSON.stringify({
      error: true,
      status: response.status,
      statusText: response.statusText
    }, null, 2);
  }
  return JSON.stringify(await response.json(), null, 2);
})();
EOF
```

### Microsoft Graph API (Recommended)

**Endpoint**: `/_api/v2.0/me/drive/*`

Graph API is simpler and more reliable than SharePoint REST for file operations.

**Advantages:**
- No personal path construction needed (uses `/me` endpoint)
- Simpler URL structure
- Better error messages
- Consistent across tenant types
- Modern JSON responses

**List files:**
```bash
bash scripts/list-files-graph.sh
bash scripts/list-files-graph.sh "Documents/Subfolder"
```

**Direct API calls:**
```bash
# List root
cat <<EOF | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const response = await fetch("$SP_TENANT_URL/_api/v2.0/me/drive/root/children");
  const data = await response.json();
  return JSON.stringify(data.value.map(item => ({
    name: item.name,
    type: item.folder ? 'folder' : 'file',
    size: item.size,
    modified: item.lastModifiedDateTime
  })), null, 2);
})();
EOF

# List specific folder
cat <<EOF | agent-browser --session "$SESSION" eval --stdin
(async () => {
  const response = await fetch("$SP_TENANT_URL/_api/v2.0/me/drive/root:/Documents/Project:/children");
  const data = await response.json();
  return JSON.stringify(data.value, null, 2);
})();
EOF
```

## Common Operations

### List Files (Root)

**Endpoint**: `RenderListDataAsStream`

```javascript
const response = await fetch(
  `${SP_TENANT_URL}${SP_USER_PATH}/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1='${encodeURIComponent(SP_USER_PATH + '/Documents')}'&TryNewExperienceSingle=TRUE`,
  {
    method: 'POST',
    headers: {
      'Accept': 'application/json;odata=verbose',
      'Content-Type': 'application/json;odata=verbose'
    },
    body: JSON.stringify({
      parameters: {
        __metadata: { type: 'SP.RenderListDataParameters' },
        RenderOptions: 5691143
      }
    })
  }
);

const data = await response.json();
const files = data.ListData.Row.map(item => ({
  name: item.FileLeafRef,
  type: item.FSObjType === '1' ? 'folder' : 'file',
  size: parseInt(item.SMTotalSize || 0),
  modified: item['Modified.'],
  fileType: item['File_x0020_Type'] || 'folder',
  path: item.FileRef
}));

return files;
```

**Response Fields**:
- `FileLeafRef` → filename
- `FSObjType` → "0" (file) / "1" (folder)
- `SMTotalSize` → size in bytes (string)
- `Modified.` → ISO-8601 timestamp
- `File_x0020_Type` → extension (docx, xlsx, pdf, ...)
- `FileRef` → full server-relative path
- `UniqueId` → GUID

### List Subfolder Files

Add `FolderServerRelativeUrl` parameter:

```javascript
{
  parameters: {
    __metadata: { type: 'SP.RenderListDataParameters' },
    RenderOptions: 5691143,
    FolderServerRelativeUrl: `${SP_USER_PATH}/Documents/Projects`
  }
}
```

### Filter by File Type

Use `ViewXml` with CAML query:

```javascript
{
  parameters: {
    __metadata: { type: 'SP.RenderListDataParameters' },
    RenderOptions: 5691143,
    ViewXml: '<View><Query><Where><Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">pptx</Value></Eq></Where></Query></View>'
  }
}
```

### Pagination

```javascript
ViewXml: '<View><RowLimit>50</RowLimit></View>'
```

For subsequent pages, include `DirPagingInfo` from previous response.

### Download Files

**Direct path** (authenticated via browser session):

```javascript
const fileUrl = `${SP_TENANT_URL}${SP_USER_PATH}/Documents/report.pdf`;

// Check if exists
const headResponse = await fetch(fileUrl, { method: 'HEAD' });
if (!headResponse.ok) {
  throw new Error(`File not found: ${headResponse.status}`);
}

// Download (optional ?download=1 forces download vs preview)
const response = await fetch(`${fileUrl}?download=1`);
const blob = await response.blob();
// ... handle blob (save to file, etc.)
```

### Upload Files

Use SharePoint's `/_api/web/GetFolderByServerRelativeUrl()` endpoint:

```javascript
// 1. Read file as ArrayBuffer (in Node) or from File input (in browser)
// 2. Upload via POST

const uploadUrl = `${SP_TENANT_URL}/_api/web/GetFolderByServerRelativeUrl('${folderPath}')/Files/add(url='${filename}',overwrite=true)`;

const response = await fetch(uploadUrl, {
  method: 'POST',
  headers: {
    'Accept': 'application/json;odata=verbose',
    'Content-Type': 'application/octet-stream'
  },
  body: fileArrayBuffer
});
```

### Microsoft Graph API (SharePoint-hosted)

**Works** with browser authentication (no separate OAuth token):

```javascript
const response = await fetch(`${SP_TENANT_URL}/_api/v2.0/me/drive/root/children`);
const data = await response.json();

data.value.forEach(item => {
  console.log(item.name, item.size, item.lastModifiedDateTime);
});
```

**Does not work**: Public `https://graph.microsoft.com/v1.0/...` (requires OAuth token).

## Scripts Reference

Five bundled scripts in `scripts/`. Run with `bash scripts/<name>.sh` or copy into your project.

### session-manager.sh

Create, check, and destroy SharePoint sessions with proper profile lock handling.

```bash
bash scripts/session-manager.sh create              # Create new session
bash scripts/session-manager.sh status              # Check current session
bash scripts/session-manager.sh destroy             # Cleanup session
bash scripts/session-manager.sh cleanup             # Force cleanup (kill processes, remove locks)
```

### list-files.sh

List files and folders with filtering, pagination, and output formatting.

```bash
bash scripts/list-files.sh                          # List root
bash scripts/list-files.sh --folder "Projects"      # List subfolder
bash scripts/list-files.sh --type docx              # Filter by extension
bash scripts/list-files.sh --limit 20               # Limit results
bash scripts/list-files.sh --format json            # Output format (json|csv|table)
bash scripts/list-files.sh --modified-after "2024-01-01"  # Date filter
```

### download-file.sh

Download files from SharePoint/OneDrive.

```bash
bash scripts/download-file.sh "Documents/report.pdf"
bash scripts/download-file.sh "Documents/report.pdf" --output ~/Downloads/
bash scripts/download-file.sh "Documents/*.pdf" --batch  # Pattern matching
bash scripts/download-file.sh "Documents/big-file.zip" --resume  # Resume partial
```

### upload-file.sh

Upload files to SharePoint/OneDrive.

```bash
bash scripts/upload-file.sh local.pdf "Documents/remote.pdf"
bash scripts/upload-file.sh *.docx "Documents/Batch/"    # Batch upload
bash scripts/upload-file.sh file.pdf "Documents/" --overwrite
bash scripts/upload-file.sh file.pdf "Documents/" --rename  # Auto-rename on conflict
```

### discover-api.sh

Capture network traffic to discover new SharePoint API endpoints.

```bash
bash scripts/discover-api.sh                        # Interactive mode
bash scripts/discover-api.sh --auto --output apis.json  # Auto-navigate common pages
bash scripts/discover-api.sh --replay apis.json     # Replay captured requests
```

## Configuration

Configuration is stored in `<skill-dir>/.config` and automatically loaded by all scripts.

### Auto-Generated Configuration

Created by `provision-profile.sh`, contains:

| Variable | Description | Example |
|----------|-------------|---------|
| `SP_TENANT_URL` | SharePoint tenant base URL | `https://contoso.sharepoint.com` |
| `SP_USER_PATH` | Personal site path | `/personal/john_contoso_com` |
| `SP_PROFILE_PATH` | Profile directory (within skill) | `<skill-dir>/profile` |
| `SP_TENANT_TYPE` | Tenant type | `commercial`, `gcc-high`, `custom` |
| `SP_SESSION_PREFIX` | Session ID prefix | `sharepoint` |
| `SP_RENDER_OPTIONS` | API options | `5691143` |

### Environment Variable Overrides

Environment variables override `.config` values if set:

```bash
export SP_TENANT_URL="https://other-tenant.sharepoint.com"
bash scripts/list-files.sh
```

### Tenant Types

The provision wizard supports:

1. **Commercial** (`.sharepoint.com`) - Standard Microsoft 365
2. **GCC High** (`.sharepoint.us`) - US Government/Defense
3. **Custom** - Manual URL entry

See `references/tenant-types.md` for complete details.

### Re-provisioning

To change tenant or re-authenticate:

```bash
# Run provision wizard again
bash scripts/provision-profile.sh

# It will detect existing profile and prompt to overwrite
```

### Manual Configuration

Advanced users can edit `.config` directly:

```bash
# Edit configuration
vi <skill-dir>/.config

# Test
bash scripts/session-manager.sh status
```

## Troubleshooting

### Profile Lock Error

```bash
# Cleanup automatically handled by session-manager
bash scripts/session-manager.sh cleanup
```

### 401 Unauthorized

- Profile authentication expired → Re-authenticate manually
- Wrong tenant URL → Verify `SP_TENANT_URL`
- Tenant type mismatch → Check `.com` vs `.us`

### CAML Query Syntax Error

- XML must be well-formed
- Field names are case-sensitive
- Use `_x0020_` for spaces in field names (e.g., `File_x0020_Type`)

### Rate Limiting / 429 Errors

SharePoint throttles aggressive requests:
- Add delays between requests (500ms-1s)
- Batch operations where possible
- Use `RenderListDataAsStream` instead of individual file queries

See `references/troubleshooting.md` for comprehensive solutions.

## API Discovery

Use HAR capture to find new endpoints:

```bash
# Start capture
agent-browser --session "$SESSION" network har start

# Navigate to SharePoint UI, perform actions
agent-browser --session "$SESSION" goto "$SP_TENANT_URL/Documents"
agent-browser --session "$SESSION" wait --load networkidle

# Stop and analyze
agent-browser --session "$SESSION" network har stop /tmp/sharepoint.har
jq '.log.entries[] | select(.request.url | contains("_api")) | {url: .request.url, method: .request.method}' /tmp/sharepoint.har
```

Or use `discover-api.sh` for automated workflow.

## Learn More

- **Authentication & profiles**: `references/authentication.md`
- **Complete API reference**: `references/api-reference.md`
- **Troubleshooting guide**: `references/troubleshooting.md`
- **Tenant type differences**: `references/tenant-types.md`
- **Microsoft SharePoint REST API**: https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest
