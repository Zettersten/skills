# SharePoint REST API Reference

Complete reference for SharePoint REST APIs used in this skill.

## RenderListDataAsStream

Primary endpoint for listing files and folders.

### Endpoint Format

```
POST https://{tenant}/{user-path}/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1='{encoded-path}'&TryNewExperienceSingle=TRUE
```

### Request Headers

```
Accept: application/json;odata=verbose
Content-Type: application/json;odata=verbose
```

### Request Body

```json
{
  "parameters": {
    "__metadata": { "type": "SP.RenderListDataParameters" },
    "RenderOptions": 5691143,
    "FolderServerRelativeUrl": "/personal/user/Documents/Folder",
    "ViewXml": "<View>...</View>"
  }
}
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `RenderOptions` | int | Bitmask of data fields to return (5691143 = comprehensive) |
| `FolderServerRelativeUrl` | string | Server-relative path to subfolder |
| `ViewXml` | string | CAML query for filtering/sorting |
| `Paging` | string | "TRUE" to enable pagination |

### Response Structure

```json
{
  "ListData": {
    "Row": [
      {
        "FileLeafRef": "filename.ext",
        "FSObjType": "0",
        "SMTotalSize": "1024",
        "Modified.": "2024-01-01T12:00:00Z",
        "File_x0020_Type": "docx",
        "FileRef": "/personal/user/Documents/filename.ext",
        "UniqueId": "{GUID}",
        "Editor": [{"title": "Name", "email": "user@domain.com"}]
      }
    ],
    "NextHref": "?PageFirstRow=31"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `FileLeafRef` | string | Filename |
| `FSObjType` | string | "0" = file, "1" = folder |
| `SMTotalSize` | string | Size in bytes |
| `Modified.` | string | ISO-8601 timestamp |
| `File_x0020_Type` | string | File extension |
| `FileRef` | string | Full server-relative path |
| `UniqueId` | string | GUID identifier |
| `Editor` | array | Last modifier info |

## CAML Query Reference

ViewXml uses CAML (Collaborative Application Markup Language) for filtering.

### Basic Filter

```xml
<View>
  <Query>
    <Where>
      <Eq>
        <FieldRef Name="File_x0020_Type"/>
        <Value Type="Text">docx</Value>
      </Eq>
    </Where>
  </Query>
</View>
```

### Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `<Eq>` | Equals | File type is docx |
| `<Neq>` | Not equals | File type is not docx |
| `<Gt>` | Greater than | Size > 1MB |
| `<Lt>` | Less than | Size < 1MB |
| `<Geq>` | Greater or equal | Modified >= 2024-01-01 |
| `<Leq>` | Less or equal | Modified <= 2024-12-31 |
| `<Contains>` | Contains substring | Name contains "report" |
| `<BeginsWith>` | Starts with | Name starts with "2024" |

### Logical Operators

```xml
<!-- AND -->
<And>
  <Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">pdf</Value></Eq>
  <Geq><FieldRef Name="Modified"/><Value Type="DateTime">2024-01-01</Value></Geq>
</And>

<!-- OR -->
<Or>
  <Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">docx</Value></Eq>
  <Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">pdf</Value></Eq>
</Or>

<!-- NOT -->
<Not>
  <Eq><FieldRef Name="FSObjType"/><Value Type="Text">1</Value></Eq>
</Not>
```

### Field Name Encoding

Spaces → `_x0020_`

Examples:
- `File Type` → `File_x0020_Type`
- `Created Date` → `Created_x0020_Date`
- `Last Modified` → `Last_x0020_Modified`

### Pagination

```xml
<View>
  <RowLimit>50</RowLimit>
</View>
```

Response includes `NextHref` for next page.

## File Download

Direct path access with browser authentication.

### Endpoint

```
GET https://{tenant}/{user-path}/Documents/{filename}?download=1
```

### Parameters

| Parameter | Optional | Description |
|-----------|----------|-------------|
| `download=1` | Yes | Forces download vs preview |

### Example

```javascript
const fileUrl = `${SP_TENANT_URL}${SP_USER_PATH}/Documents/report.pdf?download=1`;
const response = await fetch(fileUrl);
const blob = await response.blob();
```

## File Upload

Upload via GetFolderByServerRelativeUrl.

### Endpoint

```
POST https://{tenant}/_api/web/GetFolderByServerRelativeUrl('{folder}')/Files/add(url='{filename}',overwrite={bool})
```

### Request Headers

```
Accept: application/json;odata=verbose
Content-Type: application/octet-stream
```

### Request Body

Binary file content (ArrayBuffer or Uint8Array).

### Example

```javascript
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

## Microsoft Graph API (SharePoint-hosted)

Works with browser authentication (no OAuth token required).

### List Root Files

```
GET https://{tenant}/_api/v2.0/me/drive/root/children
```

### Response

```json
{
  "value": [
    {
      "name": "filename.ext",
      "size": 1024,
      "lastModifiedDateTime": "2024-01-01T12:00:00Z",
      "folder": null,
      "file": { "mimeType": "application/pdf" },
      "@microsoft.graph.downloadUrl": "https://..."
    }
  ]
}
```

### Field Mappings

| Graph API | REST API | Notes |
|-----------|----------|-------|
| `name` | `FileLeafRef` | Filename |
| `size` | `SMTotalSize` | Size in bytes (number vs string) |
| `lastModifiedDateTime` | `Modified.` | ISO-8601 timestamp |
| `folder` | `FSObjType === '1'` | Folder indicator |
| `file` | `FSObjType === '0'` | File indicator |

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Bad Request | Check CAML syntax, field names |
| 401 | Unauthorized | Re-authenticate profile |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify path, tenant URL |
| 429 | Too Many Requests | Rate limiting - add delays |
| 500 | Server Error | Retry with exponential backoff |

## Rate Limiting

SharePoint throttles aggressive requests:

- **Per-user limit**: ~5000 requests/5 minutes
- **Per-app limit**: Higher for registered apps
- **Retry-After**: Header indicates wait time

**Best practices**:
- Batch operations
- Add delays (500ms-1s between requests)
- Use RenderListDataAsStream (1 call) vs individual queries (N calls)
