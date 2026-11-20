# MCP Approval Gate - Quick Reference

## Installation
```bash
curl -fsSL https://raw.githubusercontent.com/OWNER/mcp-approval-gate/main/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
```

## First Time Setup
```bash
# 1. Create bot in Telegram (@BotFather)
# 2. Configure
mcp-approval-gate setup

# 3. Test
mcp-approval-gate test

# 4. Guard Claude Desktop
mcp-approval-gate wrap-desktop

# 5. Install auto-start service
mcp-approval-gate install-service
```

## Daily Commands
```bash
mcp-approval-gate status          # Check if running
mcp-approval-gate renew           # Extend session 24h
mcp-approval-gate activity        # View history
```

## How It Works

```
Claude Desktop → Approval Gate → Telegram → You (tap Allow/Block)
                      ↓
               Real MCP Server (if approved)
```

## File Locations
- Config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- State: `~/Library/Application Support/MCPApprovalGate/`
- Service: `~/Library/LaunchAgents/com.mcpapprovalgate.daemon.plist`

## Troubleshooting
```bash
# Daemon not running
mcp-approval-gate daemon

# Session expired
mcp-approval-gate renew

# View logs
cat ~/Library/Application\ Support/MCPApprovalGate/daemon.log

# Complete reset
mcp-approval-gate uninstall --purge
```

## Status Indicators
- 🔒 guarded = Protected by approval gate
- 🚫 UNGUARDED = Direct access, no approval needed
- ✅ Approvals ON = Session active
- ❌ Approvals OFF = Session expired, renew needed
