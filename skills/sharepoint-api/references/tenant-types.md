# SharePoint Tenant Types

Differences between Commercial, GCC, and GCC High SharePoint tenants.

## Tenant Type Overview

| Type | Domain | Audience | Authentication |
|------|--------|----------|----------------|
| Commercial | `.sharepoint.com` | Public/Private sector | Standard Microsoft 365 |
| GCC | `.sharepoint.com` | US Government | GCC credentials |
| GCC High | `.sharepoint.us` | DoD/Defense contractors | GCC High credentials |

## Commercial (.sharepoint.com)

Standard SharePoint Online for commercial and public sector organizations.

### Configuration

```bash
export SP_TENANT_URL="https://contoso.sharepoint.com"
export SP_USER_PATH="/personal/john_contoso_com"
export SP_PROFILE_PATH="~/agent-browser-profiles/contoso-profile"
```

### URL Format

- **Tenant**: `https://TENANT.sharepoint.com`
- **User path**: `/personal/USER_TENANT_com`
- **Documents**: `/personal/USER_TENANT_com/Documents`

### Features

- All SharePoint REST APIs available
- SharePoint-hosted Graph API works
- Public Graph API works (with OAuth)
- Full feature parity

### Example

```bash
# Commercial tenant: Contoso
export SP_TENANT_URL="https://contoso.sharepoint.com"
export SP_USER_PATH="/personal/john_contoso_com"

# List files
bash scripts/list-files.sh
```

## GCC (.sharepoint.com)

Government Community Cloud for US government agencies.

### Configuration

```bash
export SP_TENANT_URL="https://agency.sharepoint.com"
export SP_USER_PATH="/personal/john_agency_onmicrosoft_com"
export SP_PROFILE_PATH="~/agent-browser-profiles/gcc-profile"
```

### URL Format

- **Tenant**: `https://TENANT.sharepoint.com`
- **User path**: `/personal/USER_TENANT_onmicrosoft_com` (note: `onmicrosoft.com`)
- **Documents**: `/personal/USER_TENANT_onmicrosoft_com/Documents`

### Differences from Commercial

- Same domain (`.sharepoint.com`)
- Different user path suffix (`onmicrosoft.com`)
- Separate authentication realm
- Reduced Graph API surface

### Features

- SharePoint REST APIs available
- SharePoint-hosted Graph API works
- Public Graph API limited
- Some features delayed vs Commercial

## GCC High (.sharepoint.us)

Government Community Cloud High for DoD and defense contractors.

### Configuration

```bash
export SP_TENANT_URL="https://agency.sharepoint.us"
export SP_USER_PATH="/personal/john_agency_onmicrosoft_us"
export SP_PROFILE_PATH="~/agent-browser-profiles/gcc-high-profile"
```

### URL Format

- **Tenant**: `https://TENANT.sharepoint.us` (note: `.us` not `.com`)
- **User path**: `/personal/USER_TENANT_onmicrosoft_us` (note: `.us` suffix)
- **Documents**: `/personal/USER_TENANT_onmicrosoft_us/Documents`

### Key Differences

- **Domain**: `.sharepoint.us` (completely different)
- **Separate infrastructure**: Isolated from Commercial
- **Credentials**: Cannot share with Commercial accounts
- **Profile**: Requires separate agent-browser profile

### Features

- SharePoint REST APIs available
- SharePoint-hosted Graph API works
- Public Graph API not available
- Feature updates lag Commercial by months

### Example

```bash
# GCC High tenant: HawkEye 360
export SP_TENANT_URL="https://he360-my.sharepoint.us"
export SP_USER_PATH="/personal/erik_zettersten_he360_onmicrosoft_us"

# List files
bash scripts/list-files.sh
```

## API Availability Matrix

| API | Commercial | GCC | GCC High |
|-----|------------|-----|----------|
| RenderListDataAsStream | ✅ | ✅ | ✅ |
| Direct file download | ✅ | ✅ | ✅ |
| File upload | ✅ | ✅ | ✅ |
| SharePoint-hosted Graph (`/_api/v2.0/*`) | ✅ | ✅ | ✅ |
| Public Graph (`graph.microsoft.com`) | ✅ | ⚠️ Limited | ❌ |
| Search API | ✅ | ✅ | ✅ |
| Webhooks | ✅ | ⚠️ Limited | ❌ |

✅ = Fully available  
⚠️ = Limited functionality  
❌ = Not available

## Migration Between Tenant Types

### Cannot Migrate Profiles

Profiles are tenant-specific and cannot be reused:

```bash
# Wrong - using Commercial profile for GCC High
export SP_TENANT_URL="https://agency.sharepoint.us"  # GCC High
export SP_PROFILE_PATH="~/agent-browser-profiles/commercial-profile"  # Commercial

# Correct - separate profiles
export SP_TENANT_URL="https://agency.sharepoint.us"
export SP_PROFILE_PATH="~/agent-browser-profiles/gcc-high-profile"
```

### Migration Checklist

1. **Create new profile**:
   ```bash
   mkdir -p ~/agent-browser-profiles/NEW-profile
   ```

2. **Update environment variables**:
   ```bash
   export SP_TENANT_URL="https://NEW-TENANT.sharepoint.{com|us}"
   export SP_USER_PATH="/personal/NEW_USER_..."
   export SP_PROFILE_PATH="~/agent-browser-profiles/NEW-profile"
   ```

3. **Authenticate**:
   ```bash
   bash scripts/session-manager.sh create
   ```

4. **Test**:
   ```bash
   bash scripts/list-files.sh --limit 5
   ```

## Multi-Tenant Support

Managing multiple tenants simultaneously:

```bash
# Function to switch tenants
switch_tenant() {
  local tenant_name="$1"
  
  case "$tenant_name" in
    commercial)
      export SP_TENANT_URL="https://contoso.sharepoint.com"
      export SP_USER_PATH="/personal/john_contoso_com"
      export SP_PROFILE_PATH="~/agent-browser-profiles/contoso-profile"
      ;;
    gcc-high)
      export SP_TENANT_URL="https://agency.sharepoint.us"
      export SP_USER_PATH="/personal/john_agency_onmicrosoft_us"
      export SP_PROFILE_PATH="~/agent-browser-profiles/gcc-high-profile"
      ;;
    *)
      echo "Unknown tenant: $tenant_name" >&2
      return 1
      ;;
  esac
  
  echo "Switched to: $tenant_name"
  echo "Tenant URL: $SP_TENANT_URL"
}

# Usage
switch_tenant commercial
bash scripts/list-files.sh

switch_tenant gcc-high
bash scripts/list-files.sh
```

## Determining Your Tenant Type

Don't know your tenant type?

1. **Check URL**:
   - `.sharepoint.com` → Commercial or GCC
   - `.sharepoint.us` → GCC High

2. **Check admin portal**:
   - Commercial: `admin.microsoft.com`
   - GCC: `gcc.admin.microsoft.com`
   - GCC High: `admin.gcc.microsoft.us`

3. **Ask your IT admin**

## Best Practices

1. **Separate profiles** - One per tenant type
2. **Name profiles descriptively** - Include tenant name
3. **Document tenant type** - In scripts and configs
4. **Test after migration** - Verify APIs work
5. **Handle gracefully** - Check response codes, tenant-specific errors
