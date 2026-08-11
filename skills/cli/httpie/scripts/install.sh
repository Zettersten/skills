#!/usr/bin/env bash
# install.sh — Install httpie without admin/root permissions
#
# Install order by platform:
#   macOS:   Homebrew → pipx → pip --user
#   Linux:   pipx → pip --user → snap (user mode)
#   Windows: pip --user (Git Bash / WSL)
#
# Usage:
#   bash install.sh
#   bash install.sh --force   # reinstall even if already present

set -euo pipefail

FORCE=0
[[ "${1:-}" == "--force" ]] && FORCE=1

# ── Helpers ───────────────────────────────────────────────────────────────────

cmd() { command -v "$1" &>/dev/null; }

info()    { printf '\033[34m→\033[0m  %s\n' "$*"; }
success() { printf '\033[32m✓\033[0m  %s\n' "$*"; }
warn()    { printf '\033[33m!\033[0m  %s\n' "$*" >&2; }
die()     { printf '\033[31m✗\033[0m  %s\n' "$*" >&2; exit 1; }

path_hint() {
  local bin_dir="$1"
  warn "Add $bin_dir to your PATH if http isn't found after install:"
  case "$SHELL" in
    */zsh)  warn "  echo 'export PATH=\"$bin_dir:\$PATH\"' >> ~/.zshrc && source ~/.zshrc" ;;
    */fish) warn "  fish_add_path $bin_dir" ;;
    *)      warn "  echo 'export PATH=\"$bin_dir:\$PATH\"' >> ~/.bashrc && source ~/.bashrc" ;;
  esac
}

# ── Already installed? ────────────────────────────────────────────────────────

if cmd http && [[ "$FORCE" -eq 0 ]]; then
  success "httpie already installed: $(http --version 2>/dev/null | head -1)"
  exit 0
fi

info "Installing httpie (no admin permissions required)..."

OS="$(uname -s)"

# ── macOS ─────────────────────────────────────────────────────────────────────

if [[ "$OS" == "Darwin" ]]; then
  if cmd brew; then
    info "Using Homebrew..."
    brew install httpie
  elif cmd pipx; then
    info "Using pipx..."
    pipx install httpie
  elif cmd pip3; then
    info "Using pip3 --user..."
    pip3 install --user httpie
    BIN_DIR="$(python3 -m site --user-base 2>/dev/null)/bin"
    path_hint "$BIN_DIR"
  elif cmd pip; then
    pip install --user httpie
    BIN_DIR="$(python -m site --user-base 2>/dev/null)/bin"
    path_hint "$BIN_DIR"
  else
    die "No installer found. Install Homebrew (https://brew.sh) or Python, then re-run."
  fi

# ── Linux ─────────────────────────────────────────────────────────────────────

elif [[ "$OS" == "Linux" ]]; then
  if cmd pipx; then
    info "Using pipx..."
    pipx install httpie
  elif cmd pip3; then
    info "Using pip3 --user..."
    pip3 install --user httpie
    path_hint "$HOME/.local/bin"
  elif cmd pip; then
    pip install --user httpie
    path_hint "$HOME/.local/bin"
  elif cmd snap; then
    info "Using snap..."
    snap install httpie
  else
    # Last resort: bootstrap pip via ensurepip, then install user-local
    info "Bootstrapping pip via ensurepip..."
    python3 -m ensurepip --user 2>/dev/null || die "Could not bootstrap pip. Install python3-pip or pipx."
    python3 -m pip install --user --upgrade pip
    python3 -m pip install --user httpie
    path_hint "$HOME/.local/bin"
  fi

# ── Windows / Git Bash / WSL ──────────────────────────────────────────────────

elif [[ "$OS" == MINGW* ]] || [[ "$OS" == CYGWIN* ]] || [[ "$OS" == MSYS* ]]; then
  if cmd pip; then
    info "Using pip --user..."
    pip install --user httpie
    warn "You may need to add the Python Scripts directory to your PATH."
    warn "Run: python -m site --user-scripts"
  elif cmd pip3; then
    pip3 install --user httpie
  else
    die "pip not found. Install Python from https://python.org (check 'Add to PATH' during setup)."
  fi

else
  # Fallback: try pip regardless
  warn "Unrecognised OS ($OS), attempting pip install..."
  if cmd pip3; then
    pip3 install --user httpie
  elif cmd pip; then
    pip install --user httpie
  else
    die "Could not install httpie. Please install manually: https://httpie.io/docs/cli/installation"
  fi
fi

# ── Verify ────────────────────────────────────────────────────────────────────

echo ""
if cmd http; then
  success "httpie installed: $(http --version 2>/dev/null | head -1)"
else
  warn "http command not found in PATH yet."
  warn "Restart your shell or source your profile, then run: http --version"
fi
