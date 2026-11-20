#!/usr/bin/env bash
# MCP Approval Gate installer (macOS / Linux).
#
#   From a clone:   ./install.sh
#   From PyPI:      curl -fsSL https://raw.githubusercontent.com/Adarshagnihotri0/mcp-approval-gate/main/install.sh | bash
#
# Installs into a private virtual environment (no sudo, nothing touches system Python),
# links the `mcp-approval-gate` command into ~/.local/bin, then runs the guided quickstart.
#
# Environment overrides:
#   MCP_GATE_HOME     install folder            (default: ~/.local/share/mcp-approval-gate)
#   MCP_GATE_SOURCE   what pip installs         (default: this clone if present, else "mcp-approval-gate" from PyPI)
#   MCP_GATE_PYTHON   Python 3.10+ interpreter  (default: first suitable python3.x on PATH)
#   MCP_GATE_NO_QUICKSTART=1   install only
set -euo pipefail

APP_HOME="${MCP_GATE_HOME:-$HOME/.local/share/mcp-approval-gate}"
BIN_DIR="$HOME/.local/bin"
say()  { printf '\033[1m%s\033[0m\n' "$*"; }
fail() { printf '\033[31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

case "$(uname -s)" in
  Darwin|Linux) ;;
  *) fail "This installer supports macOS and Linux. On Windows, install with: pip install mcp-approval-gate" ;;
esac

# --- find Python 3.10+ ------------------------------------------------------------------
find_python() {
  local candidate
  for candidate in "${MCP_GATE_PYTHON:-}" python3.13 python3.12 python3.11 python3.10 python3; do
    [ -n "$candidate" ] || continue
    command -v "$candidate" >/dev/null 2>&1 || continue
    if "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))' 2>/dev/null; then
      command -v "$candidate"; return 0
    fi
  done
  return 1
}
PYTHON="$(find_python)" || fail "Python 3.10 or newer is required.
  macOS:  brew install python@3.12   (or download from https://www.python.org/downloads/)
  Linux:  sudo apt install python3 python3-venv   (or your distro's equivalent)"
say "Using $("$PYTHON" -c 'import sys; print(sys.executable, sys.version.split()[0])')"

# --- choose what to install -------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ -n "${MCP_GATE_SOURCE:-}" ]; then
  SOURCE="$MCP_GATE_SOURCE"
elif [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/pyproject.toml" ] && [ -d "$SCRIPT_DIR/src/mcp_approval_gate" ]; then
  SOURCE="$SCRIPT_DIR"
else
  SOURCE="mcp-approval-gate"
fi

# --- private virtual environment --------------------------------------------------------
mkdir -p "$APP_HOME"
chmod 700 "$APP_HOME"
if [ ! -x "$APP_HOME/venv/bin/python" ]; then
  say "Creating virtual environment in $APP_HOME/venv"
  "$PYTHON" -m venv "$APP_HOME/venv" || fail "Could not create a virtual environment (Linux: install python3-venv)."
fi
say "Installing mcp-approval-gate from: $SOURCE"
"$APP_HOME/venv/bin/python" -m pip install --quiet --upgrade pip || true  # best effort
"$APP_HOME/venv/bin/python" -m pip install --quiet --upgrade "$SOURCE"

mkdir -p "$BIN_DIR"
ln -sf "$APP_HOME/venv/bin/mcp-approval-gate" "$BIN_DIR/mcp-approval-gate"
say "✓ Installed $("$BIN_DIR/mcp-approval-gate" --version)"

case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) printf '\n⚠  %s is not on your PATH. Add this to your shell profile:\n    export PATH="%s:$PATH"\n\n' "$BIN_DIR" "$BIN_DIR" ;;
esac

if [ "${MCP_GATE_NO_QUICKSTART:-0}" != "1" ]; then
  if [ -t 0 ] || [ -e /dev/tty ]; then
    exec "$BIN_DIR/mcp-approval-gate" quickstart </dev/tty
  fi
  say "Next: run  mcp-approval-gate quickstart"
fi
