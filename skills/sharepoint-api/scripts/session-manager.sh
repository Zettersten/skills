#!/usr/bin/env bash
set -euo pipefail

# session-manager.sh - SharePoint session lifecycle management
#
# Manages agent-browser sessions for SharePoint/OneDrive automation,
# handling profile locks and process cleanup safely.

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/.config"
PROFILE_DIR="$SKILL_DIR/profile"

# Load configuration if exists
if [[ -f "$CONFIG_FILE" ]]; then
  source "$CONFIG_FILE"
fi

# Configuration from environment (can override config file)
SP_TENANT_URL="${SP_TENANT_URL:-}"
SP_PROFILE_PATH="${SP_PROFILE_PATH:-$PROFILE_DIR}"
SP_SESSION_PREFIX="${SP_SESSION_PREFIX:-sharepoint}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Usage
usage() {
  cat <<EOF
Usage: $0 <command>

SharePoint session lifecycle management for agent-browser.

Commands:
  create    Create new session (kills existing processes, removes locks)
  status    Check session status and authentication
  destroy   Close browser and cleanup session
  cleanup   Force cleanup (kill all processes, remove all locks)
  help      Show this help message

Environment Variables:
  SP_TENANT_URL      SharePoint tenant base URL (required)
  SP_PROFILE_PATH    agent-browser profile directory (required)
  SP_SESSION_PREFIX  Session ID prefix (default: sharepoint)
  AGENT_BROWSER_SESSION  Current session ID (set by create)

Examples:
  # Create session
  bash $0 create

  # Check status
  bash $0 status

  # Destroy session
  bash $0 destroy

  # Force cleanup
  bash $0 cleanup
EOF
}

# Check if profile needs provisioning
check_profile() {
  if [[ ! -f "$CONFIG_FILE" ]] || [[ ! -d "$PROFILE_DIR" ]]; then
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Profile Not Provisioned${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════${NC}"
    echo ""
    echo "This skill requires a SharePoint browser profile to be provisioned."
    echo "The profile will be created in the skill directory:"
    echo "  $PROFILE_DIR"
    echo ""
    echo "Configuration will be saved to:"
    echo "  $CONFIG_FILE"
    echo ""
    read -p "Would you like to provision a profile now? [Y/n] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Nn]$ ]]; then
      echo "Profile provisioning skipped."
      echo ""
      echo "To provision later, run:"
      echo "  bash $SCRIPT_DIR/provision-profile.sh"
      exit 1
    fi

    # Run provision wizard
    bash "$SCRIPT_DIR/provision-profile.sh"

    # Reload configuration
    if [[ -f "$CONFIG_FILE" ]]; then
      source "$CONFIG_FILE"
    else
      echo -e "${RED}Error: Provisioning did not create config file${NC}" >&2
      exit 1
    fi
  fi
}

# Validate configuration
validate_config() {
  local errors=()

  if [[ -z "$SP_TENANT_URL" ]]; then
    errors+=("SP_TENANT_URL not set")
  fi

  if [[ -z "$SP_PROFILE_PATH" ]]; then
    errors+=("SP_PROFILE_PATH not set")
  fi

  if [[ ${#errors[@]} -gt 0 ]]; then
    echo -e "${RED}Error: Missing required configuration:${NC}" >&2
    for error in "${errors[@]}"; do
      echo "  - $error" >&2
    done
    echo "" >&2
    echo "Run provisioning wizard:" >&2
    echo "  bash $SCRIPT_DIR/provision-profile.sh" >&2
    exit 1
  fi
}

# Kill existing processes using profile
kill_existing_processes() {
  local profile_path="$1"

  echo "Checking for existing processes using profile..."

  # Find processes using this profile
  local pids=$(ps aux | grep -F "$profile_path" | grep -v grep | awk '{print $2}')

  if [[ -n "$pids" ]]; then
    echo "Found processes: $pids"
    echo "Killing processes..."
    echo "$pids" | xargs kill -9 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}Processes killed${NC}"
  else
    echo "No existing processes found"
  fi
}

# Remove profile locks
remove_locks() {
  local profile_path="$1"

  echo "Removing profile locks..."

  if [[ -f "$profile_path/SingletonLock" ]]; then
    rm -f "$profile_path/SingletonLock" 2>/dev/null || true
    echo -e "${GREEN}SingletonLock removed${NC}"
  else
    echo "No locks found"
  fi
}

# Create session
create_session() {
  # Check if profile needs provisioning
  check_profile

  validate_config

  echo -e "${YELLOW}Creating SharePoint session...${NC}"
  echo "Tenant: $SP_TENANT_URL"
  echo "Profile: $SP_PROFILE_PATH"
  echo ""

  # Kill existing processes
  kill_existing_processes "$SP_PROFILE_PATH"

  # Remove locks
  remove_locks "$SP_PROFILE_PATH"

  # Generate session ID
  local session_id
  session_id="$(agent-browser session id --scope worktree --prefix "$SP_SESSION_PREFIX" 2>/dev/null || echo "")"

  if [[ -z "$session_id" ]]; then
    echo -e "${RED}Error: Failed to generate session ID${NC}" >&2
    echo "Is agent-browser installed? Try: npm install -g agent-browser" >&2
    exit 1
  fi

  echo "Session ID: $session_id"
  export AGENT_BROWSER_SESSION="$session_id"

  # Open tenant
  echo "Opening tenant..."
  if agent-browser --session "$session_id" --profile "$SP_PROFILE_PATH" open "$SP_TENANT_URL" 2>&1 | grep -q "✓"; then
    echo -e "${GREEN}✓ Session created successfully${NC}"
    echo ""
    echo "Export session ID to environment:"
    echo "  export AGENT_BROWSER_SESSION=\"$session_id\""
    echo ""
    echo "Or add to your shell:"
    echo "  echo 'export AGENT_BROWSER_SESSION=\"$session_id\"' >> ~/.bashrc"
  else
    echo -e "${RED}Error: Failed to open tenant${NC}" >&2
    echo "Check your SP_TENANT_URL and SP_PROFILE_PATH" >&2
    exit 1
  fi
}

# Check session status
check_status() {
  if [[ -z "${AGENT_BROWSER_SESSION:-}" ]]; then
    echo -e "${YELLOW}No active session${NC}"
    echo "AGENT_BROWSER_SESSION environment variable not set"
    echo ""
    echo "Create a session with: $0 create"
    exit 1
  fi

  echo "Session ID: $AGENT_BROWSER_SESSION"
  echo "Tenant: ${SP_TENANT_URL:-not set}"
  echo "Profile: ${SP_PROFILE_PATH:-not set}"
  echo ""

  # Check if browser is running
  local pids=$(ps aux | grep -F "$SP_PROFILE_PATH" | grep -v grep | awk '{print $2}')

  if [[ -n "$pids" ]]; then
    echo -e "${GREEN}✓ Browser running${NC} (PIDs: $pids)"
  else
    echo -e "${RED}✗ Browser not running${NC}"
  fi

  # Try to verify authentication (simple check)
  if [[ -n "$SP_TENANT_URL" ]]; then
    echo ""
    echo "Verifying authentication..."
    local tenant_url="${SP_TENANT_URL%/}"
    if cat <<EOF | agent-browser --session "$AGENT_BROWSER_SESSION" eval --stdin 2>&1 | grep -q '"ok":true'; then
(async () => {
  try {
    const response = await fetch("$tenant_url", { method: 'HEAD' });
    return JSON.stringify({ ok: response.ok, status: response.status });
  } catch (e) {
    return JSON.stringify({ ok: false, error: e.message });
  }
})();
EOF
      echo -e "${GREEN}✓ Authentication valid${NC}"
    else
      echo -e "${YELLOW}⚠ Authentication may have expired${NC}"
      echo "Re-authenticate with: $0 create"
    fi
  fi
}

# Destroy session
destroy_session() {
  if [[ -z "${AGENT_BROWSER_SESSION:-}" ]]; then
    echo -e "${YELLOW}No active session to destroy${NC}"
    exit 0
  fi

  echo "Destroying session: $AGENT_BROWSER_SESSION"

  # Close browser
  if agent-browser --session "$AGENT_BROWSER_SESSION" close 2>&1 | grep -q "✓"; then
    echo -e "${GREEN}✓ Browser closed${NC}"
  else
    echo -e "${YELLOW}⚠ Browser may already be closed${NC}"
  fi

  echo ""
  echo "Unset session variable:"
  echo "  unset AGENT_BROWSER_SESSION"
}

# Force cleanup
force_cleanup() {
  echo -e "${YELLOW}Force cleanup (all Chrome processes and locks)${NC}"
  echo ""

  # Kill all Chrome processes
  echo "Killing Chrome processes..."
  pkill -9 Chrome 2>/dev/null && echo -e "${GREEN}Chrome processes killed${NC}" || echo "No Chrome processes found"

  # Remove all SingletonLocks in agent-browser profiles
  echo ""
  echo "Removing all SingletonLocks..."
  local locks_found=0
  if [[ -d ~/agent-browser-profiles ]]; then
    while IFS= read -r -d '' lock_file; do
      rm -f "$lock_file"
      echo "  Removed: $lock_file"
      locks_found=$((locks_found + 1))
    done < <(find ~/agent-browser-profiles -name "SingletonLock" -print0 2>/dev/null)
  fi

  if [[ $locks_found -eq 0 ]]; then
    echo "No locks found"
  else
    echo -e "${GREEN}Removed $locks_found lock(s)${NC}"
  fi

  echo ""
  echo -e "${GREEN}✓ Cleanup complete${NC}"
}

# Main
main() {
  local command="${1:-}"

  case "$command" in
    create)
      create_session
      ;;
    status)
      check_status
      ;;
    destroy)
      destroy_session
      ;;
    cleanup)
      force_cleanup
      ;;
    help|--help|-h)
      usage
      ;;
    "")
      echo "Error: No command specified" >&2
      echo "" >&2
      usage
      exit 1
      ;;
    *)
      echo "Error: Unknown command '$command'" >&2
      echo "" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
