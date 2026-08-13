# SharePoint API Troubleshooting

Common errors and solutions for SharePoint API automation.

## Profile Lock Errors

### Symptom

```
Failed to create /path/to/profile/SingletonLock: File exists (17)
Failed to create a ProcessSingleton for your profile directory
```

### Cause

Multiple Chrome instances attempting to use same profile simultaneously.

### Solution

```bash
# Use session-manager cleanup (handles locks automatically)
bash scripts/session-manager.sh cleanup
```

### Prevention

Always use session-manager.sh which handles cleanup automatically.

## Authentication Failures

### 401 Unauthorized

**Symptoms**: API calls return 401 status.

**Causes**:
- Profile authentication expired
- Wrong tenant URL
- Cookies cleared

**Solutions**:
1. Re-provision profile:
   ```bash
   bash scripts/provision-profile.sh
   # Complete wizard and re-authenticate
   ```

2. Verify tenant URL (in .config file):
   ```bash
   echo $SP_TENANT_URL
   # Should match: https://TENANT.sharepoint.com (or .us for GCC High)
   ```

3. Check session status:
   ```bash
   bash scripts/session-manager.sh status
   ```

### 403 Forbidden

**Symptoms**: API calls return 403 status.

**Causes**:
- Insufficient permissions
- Site/library access denied
- Conditional access policies

**Solutions**:
1. Verify permissions in SharePoint UI
2. Check user has access to target library
3. Contact admin if conditional access blocking automation

## CAML Query Errors

### 400 Bad Request with ViewXml

**Symptoms**: RenderListDataAsStream returns 400 when ViewXml parameter included.

**Causes**:
- Invalid XML syntax
- Wrong field names
- Incorrect field types

**Solutions**:

1. **Validate XML**:
   ```bash
   # Test with simple query first
   ViewXml='<View><RowLimit>5</RowLimit></View>'
   ```

2. **Check field name encoding**:
   ```xml
   <!-- Wrong -->
   <FieldRef Name="File Type"/>

   <!-- Correct -->
   <FieldRef Name="File_x0020_Type"/>
   ```

3. **Case sensitivity**:
   ```xml
   <!-- Wrong -->
   <FieldRef Name="file_x0020_type"/>

   <!-- Correct -->
   <FieldRef Name="File_x0020_Type"/>
   ```

4. **Valid XML**:
   ```xml
   <!-- Missing closing tag - WRONG -->
   <View><Query><Where><Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">pdf</Value></Where></Query></View>

   <!-- Properly closed - CORRECT -->
   <View><Query><Where><Eq><FieldRef Name="File_x0020_Type"/><Value Type="Text">pdf</Value></Eq></Where></Query></View>
   ```

## Rate Limiting (429 Errors)

### Symptoms

```
HTTP 429 Too Many Requests
Retry-After: 300
```

### Causes

SharePoint throttles aggressive API usage:
- Too many requests per user
- Burst traffic patterns
- Large batch operations

### Solutions

1. **Add delays**:
   ```bash
   # Between API calls
   sleep 0.5  # 500ms delay
   ```

2. **Respect Retry-After header**:
   ```javascript
   if (response.status === 429) {
     const retryAfter = parseInt(response.headers.get('Retry-After'));
     await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
   }
   ```

3. **Use efficient APIs**:
   - RenderListDataAsStream (1 call) vs individual file queries (N calls)
   - Batch operations where possible

4. **Spread operations**:
   - Don't process 1000 files in tight loop
   - Chunk into batches with delays

## Path Encoding Issues

### Symptoms

- 404 errors for valid paths
- Special characters in filenames cause failures

### Solutions

Always encode paths:

```javascript
// Wrong
const path = '/personal/user/Documents/File (1).pdf';

// Correct
const path = encodeURIComponent('/personal/user/Documents/File (1).pdf');
```

Common special characters requiring encoding:
- Spaces: ` ` → `%20`
- Parentheses: `()` → `%28%29`
- Ampersands: `&` → `%26`
- Hash: `#` → `%23`

## JavaScript Eval Errors

### Async/Await Syntax

**Wrong**:
```javascript
// Missing async wrapper
const response = await fetch(url);
```

**Correct**:
```javascript
// Wrapped in async IIFE
(async () => {
  const response = await fetch(url);
  return result;
})();
```

### JSON Parsing

**Wrong**:
```javascript
const data = response.json();  // Returns Promise
return data.ListData.Row;      // Error: undefined
```

**Correct**:
```javascript
const data = await response.json();  // Awaits Promise
return data.ListData.Row;            // Works
```

### Error Handling

Always check response.ok:

```javascript
const response = await fetch(url, options);
if (!response.ok) {
  return JSON.stringify({
    error: true,
    status: response.status,
    statusText: response.statusText
  });
}
const data = await response.json();
```

## Tenant Type Mismatch

### Symptoms

- Redirects to login page
- 404 errors for valid URLs
- Authentication fails

### Cause

Using Commercial URL for GCC High tenant (or vice versa).

### Solution

Verify tenant type:

**Commercial**:
```bash
export SP_TENANT_URL="https://contoso.sharepoint.com"
export SP_USER_PATH="/personal/john_contoso_com"
```

**GCC High**:
```bash
export SP_TENANT_URL="https://agency.sharepoint.us"
export SP_USER_PATH="/personal/john_agency_onmicrosoft_us"
```

Note: `.com` vs `.us` domain.

## Session Not Found

### Symptoms

```
Error: AGENT_BROWSER_SESSION not set
Failed to connect to session
```

### Solution

Create or export session:

```bash
# Create new session
bash scripts/session-manager.sh create

# Or export existing
export AGENT_BROWSER_SESSION="sharepoint-a1b2c3d4"
```

## Profile Provisioning Issues

### Wizard Hangs During Authentication

**Symptom**: Browser opens but wizard waits indefinitely

**Cause**: Forgot to close browser after authentication

**Solution**: Close browser window or press Ctrl+C in terminal

### Profile Not Found After Provisioning

**Symptom**: Scripts report "profile not provisioned" after running wizard

**Cause**: Wizard exited early or config file not created

**Solution**: Check for `.config` file
```bash
ls -la .config profile/

# If missing, re-run wizard
bash scripts/provision-profile.sh
```

### Wrong Tenant Type Selected

**Symptom**: Authentication works but API calls fail

**Cause**: Selected Commercial when using GCC High (or vice versa)

**Solution**: Re-provision with correct tenant type
```bash
bash scripts/provision-profile.sh
# Answer 'y' to overwrite
# Select correct type
```

## Debugging Tips

### Check Configuration

```bash
# View current configuration
cat .config

# Verify profile exists
ls -la profile/
```

### Check Session Status

```bash
# Comprehensive status check
bash scripts/session-manager.sh status
```

### Capture HAR

```bash
# Record network traffic
bash scripts/discover-api.sh /tmp/debug.har

# Analyze
jq '.log.entries[] | {url, status: .response.status}' /tmp/debug.har
```

### Test Authentication

```bash
# Load configuration
source .config

# Simple connectivity test
cat <<'EOF' | agent-browser --session "$AGENT_BROWSER_SESSION" eval --stdin
(async () => {
  const response = await fetch(process.env.SP_TENANT_URL, { method: 'HEAD' });
  return JSON.stringify({ ok: response.ok, status: response.status });
})();
EOF
```

Expected: `{"ok":true,"status":200}`

## Getting Help

1. **Check SKILL.md** - Quick reference
2. **Review api-reference.md** - Complete API docs
3. **Test with curl** - Isolate issue
4. **Capture HAR** - See actual requests
5. **Check SharePoint audit logs** - Verify requests reaching server
