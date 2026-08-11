---
name: httpie
description: Make HTTP requests using the HTTPie CLI (`http` and `https` commands). Use this skill whenever the user wants to send HTTP requests from the terminal, test or debug APIs, scrape HTML or web content, upload files, use bearer/basic/digest authentication, download files, manage sessions, watch/poll an endpoint, or convert curl commands to HTTPie syntax. Also triggers for tasks like "call this API from the terminal", "make a POST request with JSON", "send a request with an auth token", "fetch the HTML from this page", "check if this endpoint is up", or "test this endpoint".
license: MIT
compatibility: Requires httpie >= 3.0. Install with `brew install httpie` (macOS) or `pip install httpie`.
metadata:
  author: Zettersten
  version: "1.0"
  docs: https://httpie.io/docs/cli
---

# HTTPie CLI

HTTPie (`http` / `https`) is a human-friendly CLI HTTP client. It defaults to colorized, formatted output and expressive shorthand syntax.

## Synopsis

```
http [flags] [METHOD] URL [ITEM ...]
https [flags] [METHOD] URL [ITEM ...]
```

`https` is identical to `http` but defaults the scheme to `https://`.

## Method defaults

Omit METHOD and HTTPie infers it:
- No body → `GET`
- Body present → `POST`

```bash
http pie.dev/get            # GET
http pie.dev/post name=John # POST
```

## Request item operators

Items are positional arguments after the URL. The operator determines type:

| Syntax | Type | Example |
|--------|------|---------|
| `key=value` | JSON string field | `name=John` |
| `key:=json` | Raw JSON value | `active:=true` `count:=42` `tags:='["a","b"]'` |
| `key==value` | Query string param | `q==httpie per_page==10` |
| `key:value` | HTTP header | `X-Token:abc Authorization:"Bearer token"` |
| `key@file` | File upload (multipart) | `avatar@photo.jpg` |
| `key=@file` | String from file | `body=@payload.txt` |
| `key:=@file` | JSON from file | `data:=@config.json` |

## JSON requests (default)

```bash
# POST with JSON body
http POST api.example.com/users name=Alice age:=30 admin:=false

# Nested JSON — use single quotes to protect shell expansion
http POST api.example.com/users address:='{"city":"NYC","zip":"10001"}'

# PUT with JSON
http PUT api.example.com/users/1 name=Bob
```

## Form data

Add `-f` (`--form`) to send `application/x-www-form-urlencoded` instead of JSON:

```bash
http -f POST api.example.com/login username=alice password=secret
```

## File uploads (multipart)

Use `key@file` items. HTTPie automatically sets `Content-Type: multipart/form-data`.

```bash
http -f POST api.example.com/upload file@report.pdf
http -f POST api.example.com/upload file@image.png name=headshot
```

## Query parameters

Append `key==value` to avoid shell-quoting `&`:

```bash
http https://api.github.com/search/repositories q==httpie sort==stars per_page==5
```

## HTTP headers

```bash
# Set headers with Key:Value
http GET api.example.com/data Accept:application/json X-Request-Id:abc123

# Common pattern: Content-Type is set automatically for JSON/form, but you can override
http POST api.example.com/data Content-Type:text/plain < body.txt
```

## Authentication

### Basic auth

```bash
http -a username:password api.example.com/private
# or
http --auth=username:password api.example.com/private
```

### Bearer token

```bash
http --auth-type=bearer --auth=TOKEN api.example.com/private
```

### Digest auth

```bash
http --auth-type=digest --auth=username:password api.example.com/private
```

### API key via header (most common for REST APIs)

```bash
http api.example.com/data Authorization:"Bearer $TOKEN"
http api.example.com/data X-API-Key:$API_KEY
```

## Output control

| Flag | What it prints |
|------|----------------|
| `-v` | Request + response headers and body (verbose) |
| `-h` | Response headers only |
| `-b` | Response body only (default when piping) |
| `--print=HhBb` | Mix: H=request headers, h=response headers, B=request body, b=response body |
| `--offline` | Build and print the request without sending it |

```bash
# Debug: see exactly what's being sent
http -v POST api.example.com/endpoint name=test

# Check headers only
http -h api.example.com/data

# Preview request without sending
http --offline POST api.example.com/users name=Alice
```

## Downloads

```bash
# Save with server-suggested filename
http --download pie.dev/image/png

# Save to specific file
http --download --output=image.png pie.dev/image/png

# Pipe to file (suppresses response body from terminal)
http pie.dev/image/png > image.png
```

## Sessions

Sessions persist cookies, auth credentials, and headers across requests to the same host.

```bash
# Create/use a named session (stored in ~/.config/httpie/sessions/)
http --session=myapp POST api.example.com/login username=alice password=secret

# Subsequent requests reuse the session's cookies and auth
http --session=myapp api.example.com/profile

# Read-only session (load but don't update it)
http --session-read-only=myapp api.example.com/data
```

## Raw request body

Pipe or redirect to send an arbitrary body:

```bash
# From file
http POST api.example.com/data < payload.json

# From string (bash)
echo '{"key":"value"}' | http POST api.example.com/data Content-Type:application/json
```

## HTTPS / SSL

```bash
# Use https command (sets default scheme to https://)
https api.example.com/data

# Skip certificate verification (dev/testing only)
http --verify=no https://self-signed.example.com

# Client certificate
http --cert=client.crt --cert-key=client.key https://mtls.example.com
```

## Redirects and proxies

```bash
# Follow redirects
http -F api.example.com/redirect    # or --follow

# Proxy
http --proxy=http:http://proxy:8080 api.example.com/data
```

## Streaming responses

```bash
# Stream a chunked or SSE response
http --stream api.example.com/events
```

## Gotchas

- Shell variables in headers need quoting: `Authorization:"Bearer $TOKEN"` not `Authorization:Bearer $TOKEN` (the shell will strip the space).
- `key:=value` is for raw JSON — booleans and numbers need this: `active:=true`, not `active=true` (which sends the string `"true"`).
- When piping output to another command, HTTPie suppresses color/formatting and prints only the response body. Use `-b` explicitly if you also need that behavior interactively.
- `--verify=no` skips SSL entirely — only use in development/trusted networks.
- Named sessions are per-host; `--session=dev` for `api.example.com` and `api2.example.com` are stored separately.

## Scripts

Three scripts are bundled in `scripts/`. Run them directly with `bash scripts/<name>.sh` from the skill directory, or copy them into your project.

### `scripts/install.sh` — Install httpie without admin rights

Use when: httpie is not installed, or you need a user-scoped install that doesn't require `sudo`.

Detects the platform and picks the best no-admin installer:
- macOS: Homebrew → pipx → pip --user
- Linux: pipx → pip --user → snap
- Windows/Git Bash: pip --user

Always prints a PATH hint when the binary lands somewhere that might not be in `$PATH` yet.

```bash
bash scripts/install.sh
bash scripts/install.sh --force   # reinstall even if already present
```

### `scripts/scrape.sh` — Fetch URLs with browser-like defaults

Use when: the user wants to scrape or retrieve HTML/content from a URL — especially when a bare `curl` or plain `http` call returns a 403, 429, or degraded content.

The core value: it sets the full suite of headers a real Chrome browser sends (User-Agent, Accept, Accept-Language, Cache-Control). Omitting these is the #1 reason servers block or serve different content to scripts.

```bash
bash scripts/scrape.sh https://example.com                    # raw HTML
bash scripts/scrape.sh https://example.com --text             # readable text, no tags
bash scripts/scrape.sh https://example.com --save             # save to auto-named file
bash scripts/scrape.sh https://example.com --save=page.html   # save to specific file
bash scripts/scrape.sh https://example.com --status           # just the status code
bash scripts/scrape.sh https://example.com --headers          # response headers only
bash scripts/scrape.sh https://api.example.com --json         # request JSON instead of HTML
bash scripts/scrape.sh https://example.com --session=NAME     # reuse cookies
bash scripts/scrape.sh https://example.com --no-verify        # skip SSL check

# Pipe into other tools
bash scripts/scrape.sh https://api.example.com/data --json | jq '.items[]'
bash scripts/scrape.sh https://example.com --text | grep -i 'error'
```

### `scripts/check.sh` — Endpoint health check and testing

Use when: the user wants to verify an endpoint is up, assert a specific status code or JSON value, measure response time, or watch an endpoint during a deploy/restart.

```bash
bash scripts/check.sh https://api.example.com/health
bash scripts/check.sh https://api.example.com/users --expect=201 --method=POST
bash scripts/check.sh https://api.example.com/admin --auth="Bearer $TOKEN"
bash scripts/check.sh https://api.example.com/status --json-key=.status --json-val=ok
bash scripts/check.sh https://api.example.com/health --watch          # poll every 5s
bash scripts/check.sh https://api.example.com/health --watch=10        # poll every 10s
bash scripts/check.sh https://api.example.com/health --quiet           # exit 0/1, no output
bash scripts/check.sh https://api.example.com/health --verbose         # include response body
```

Timing is color-coded: green < 200ms, yellow < 1s, red ≥ 1s. The `--json-key` assertion uses `jq` (optional — skipped gracefully if not installed).

---

## Common patterns

```bash
# GitHub API — list issues
http https://api.github.com/repos/httpie/cli/issues Authorization:"token $GITHUB_TOKEN" per_page==5

# Create a resource and capture its ID
http POST api.example.com/items name=Widget | jq '.id'

# Health check with timing info
http -h --print=H api.example.com/health

# Patch a single field
http PATCH api.example.com/users/42 email=new@example.com

# Delete a resource
http DELETE api.example.com/users/42 Authorization:"Bearer $TOKEN"
```
