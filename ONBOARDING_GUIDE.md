# MCP Approval Gate - Complete Onboarding Guide

## Overview

MCP Approval Gate is a security proxy that intercepts every MCP (Model Context Protocol) tool call from Claude Desktop, requiring your approval via **Telegram** or a **local popup** before execution.

---

## Architecture Flow

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   Claude    │────▶│  Approval Gate  │────▶│   Telegram   │────▶│     You     │
│   Desktop   │     │  (Interceptor)  │     │   (Decision) │     │  (Tap Allow │
└─────────────┘     └─────────────────┘     └──────────────┘     │   or Block) │
                           │                                      └─────────────┘
                           ▼
                    ┌──────────────┐
                    │  Real MCP    │
                    │   Server     │
                    └──────────────┘
```

---

## Installation Steps

### Step 1: Prerequisites
- macOS or Linux
- Python 3.10+
- Telegram account

### Step 2: Install

```bash
# From PyPI (recommended)
curl -fsSL https://raw.githubusercontent.com/OWNER/mcp-approval-gate/main/install.sh | bash

# Or from local clone
./install.sh
```

**What happens:**
- Creates virtual environment: `~/.local/share/mcp-approval-gate/venv`
- Links command: `~/.local/bin/mcp-approval-gate`
- Creates state directory: `~/Library/Application Support/MCPApprovalGate/`

### Step 3: Add to PATH

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

---

## Telegram Bot Setup

### Step 1: Create Bot
1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Follow prompts, choose name and username
4. **Copy the bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure

```bash
mcp-approval-gate setup
```

**Interactive prompts:**
1. Paste bot token (hidden input)
2. Open private chat with your bot
3. Send the pairing command shown
4. Your chat is now paired

### Step 3: Verify

```bash
mcp-approval-gate test
```

**Expected output:**
```
Sent. Open Telegram and tap Allow or Block…
  ✓ You tapped Allow — the gate would have forwarded the request.
```

---

## Guarding Claude Desktop

### Understanding the Flow

**Before wrapping:**
```json
{
  "mcpServers": {
    "notes": {
      "command": "python3",
      "args": ["server.py"]
    }
  }
}
```

**After wrapping:**
```json
{
  "mcpServers": {
    "guarded-notes": {
      "command": "/usr/bin/python3",
      "args": [
        "-m", "mcp_approval_gate", "stdio",
        "--server", "guarded-notes",
        "--approver", "daemon",
        "--autostart",
        "--",
        "python3", "server.py"
      ]
    }
  }
}
```

### Wrap All Servers

```bash
mcp-approval-gate wrap-desktop
```

**What happens:**
- Backs up original config (timestamped)
- Rewrites each server to route through gate
- Adds `guarded-` prefix to server names
- Starts daemon if not running

### Wrap Specific Servers

```bash
mcp-approval-gate wrap-desktop --only files,github
```

### Check Status

```bash
mcp-approval-gate status
```

**Example output:**
```
Daemon:    running, Telegram reachable
Approvals: ON (1026 min left)
Waiting:   0   Always-allow rules: 0

Claude Desktop servers:
  🔒 guarded-notes: guarded
  🔒 guarded-files: guarded
  🚫 github: UNGUARDED
```

---

## Daily Usage Flow

### 1. Start Daemon (if not using service)

```bash
mcp-approval-gate daemon
```

Or install as login service:
```bash
mcp-approval-gate install-service
```

### 2. Use Claude Normally

When Claude wants to use a tool:

1. **Request intercepted** by approval gate
2. **Telegram notification** sent to your phone
3. **You receive** a card showing:
   - Server name (e.g., `guarded-notes`)
   - Tool being called
   - Arguments (redacted for privacy)
4. **Tap Allow or Block**
5. **Claude proceeds** or is blocked

### 3. Renew Session

Sessions expire after 24 hours:

```bash
mcp-approval-gate renew
```

Or in Telegram, send `/pair <code>` to the bot.

---

## Approval Modes

| Mode | Use Case | Command |
|------|----------|---------|
| **daemon** (default) | Multiple servers, one Telegram bot | `--approver daemon` |
| **popup** | Local approval window, no Telegram | `--approver popup` |
| **telegram** | Direct polling, one server per bot | `--approver telegram` |

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `quickstart` | Guided first-time setup |
| `setup` | Telegram bot configuration |
| `test` | Send test approval |
| `status` | Check daemon and guarded servers |
| `renew` | Extend session 24 hours |
| `wrap-desktop` | Guard all Claude Desktop servers |
| `unwrap-desktop` | Restore original config |
| `activity` | View approval history |
| `daemon` | Run daemon in foreground |
| `install-service` | Auto-start at login |
| `uninstall --purge` | Complete removal |

---

## Troubleshooting

### Daemon not running
```bash
mcp-approval-gate daemon
# or
mcp-approval-gate install-service
```

### Session expired
```bash
mcp-approval-gate renew
```

### Check logs
```bash
cat ~/Library/Application\ Support/MCPApprovalGate/daemon.log
```

### Reset everything
```bash
mcp-approval-gate uninstall --purge
```

---

## File Locations

| File | Location |
|------|----------|
| Claude Desktop config | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| State directory | `~/Library/Application Support/MCPApprovalGate/` |
| Bot token | `telegram-bot-token` (in state dir) |
| Pairing config | `telegram-pairing.json` |
| Activity log | `activity.sqlite3` |
| Daemon socket | `approvals.sock` |
| launchd service | `~/Library/LaunchAgents/com.mcpapprovalgate.daemon.plist` |

---

## Security Notes

- Bot token is stored with `600` permissions (owner-only)
- All communication is local (Unix socket)
- Original config is backed up before any changes
- Session expires after 24 hours for security
- Arguments can be hidden with `--hide-inputs`

---

## Quick Start Checklist

- [ ] Install MCP approval gate
- [ ] Add `~/.local/bin` to PATH
- [ ] Create Telegram bot via @BotFather
- [ ] Run `mcp-approval-gate setup`
- [ ] Pair your private chat
- [ ] Run `mcp-approval-gate test`
- [ ] Run `mcp-approval-gate wrap-desktop`
- [ ] Install service: `mcp-approval-gate install-service`
- [ ] Ask Claude to use a tool
- [ ] Approve via Telegram

---

## Example Session

```bash
# 1. Install
$ ./install.sh
✓ Installed mcp-approval-gate 2.0.0

# 2. Setup Telegram
$ mcp-approval-gate setup
MCP Approval Gate — Telegram setup
1. In Telegram open @BotFather, send /newbot...
Bot token (hidden): ********
Private chat paired.

# 3. Test
$ mcp-approval-gate test
Sent. Open Telegram and tap Allow or Block…
  ✓ You tapped Allow

# 4. Guard Claude Desktop
$ mcp-approval-gate wrap-desktop
Backed up to: claude_desktop_config.json.bak-20241120-201500
Wrapped: notes, files

# 5. Install service
$ mcp-approval-gate install-service
Service installed. It will start at next login.

# 6. Check status
$ mcp-approval-gate status
Daemon:    running, Telegram reachable
Approvals: ON (1026 min left)
Claude Desktop servers:
  🔒 guarded-notes: guarded
  🔒 guarded-files: guarded

# 7. Use Claude - approve via Telegram when prompted!
```
