# Changelog

## 2.0.0 — 2026-11-20

### Security
- **Fixed a silent denial:** arguments heavy in `<`, `&` or quotes grew past Telegram's 4096-character limit once HTML-escaped, so the card could not be sent and the request was blocked without the user ever seeing it. The preview is now cut on the escaped text and always delivered.
- **Wider secret redaction:** `secret_key`, `aws_secret_access_key`, `connection_string`, credentials inside URLs (`user:pass@`), `?token=`/`?api_key=` query parameters, `Authorization:`/`X-Api-Key:`/`Cookie:` headers and `password=` in free text are now redacted.
- Approval daemon caps concurrent connections (128); excess connections are closed and the request denied.
- Service hardening: private umask for launchd and systemd; systemd seccomp-based restrictions.
- New `tests/test_security.py` (20 tests) including a 3,000-message fuzz of the gate.


### Added
- `quickstart`: one guided flow for Telegram pairing, background service, guarding every Claude Desktop server and a live test approval.
- `install.sh`: no-sudo installer into a private virtual environment with the `mcp-approval-gate` command.
- Shared **approval daemon**: one Telegram poller for any number of guarded servers, over a private Unix socket.
- `wrap-desktop` / `unwrap-desktop` / `status`: guard or restore every server in `claude_desktop_config.json` with backups.
- Telegram cards show **arguments with secrets redacted**, an *Always allow this tool* button, and are stamped with the outcome.
- Telegram commands `/status`, `/rules`, `/clear`, `/help`; `renew` re-enables approvals without restarting.
- `test`, `uninstall [--purge]`, `install-service`, `--version`.
- Strict typing (`mypy --strict`), `py.typed`, CI for macOS/Linux × Python 3.10–3.13, wheel build + clean install checks, PyPI trusted-publishing release workflow.
- Documentation: architecture, approach, security, testing, Claude Web and configuration guides.

### Changed
- **Breaking:** code moved into the `mcp_approval_gate` package (`src/` layout); run as `mcp-approval-gate …` or `python -m mcp_approval_gate …` instead of `python3 main.py …`. `wrap-desktop` upgrades entries written by 1.x.
- Minimum Python is 3.10 (3.9 is end-of-life).

### Removed
- Docker image and compose file: the gate must run on the user's own machine, and HTTP mode binds to loopback only, so the container could not be reached.

### Fixed
- Concurrent request test no longer assumes decision order (decisions are parallel by design).

## 1.0.0
- stdio and HTTP approval proxies, topmost local popup, single-server Telegram approvals with 24 h sessions, activity log, example notes server.
