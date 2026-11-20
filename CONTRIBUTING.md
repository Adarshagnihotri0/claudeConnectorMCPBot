# Contributing

```bash
git clone https://github.com/Adarshagnihotri0/mcp-approval-gate.git && cd mcp-approval-gate
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python -m unittest discover -s tests -v
mypy
```

Ground rules:

- **Fail closed.** Any new code path that can't positively establish an Allow must deny.
- **No runtime dependencies.** Standard library only; dev tools go in the `dev` extra.
- **`mypy --strict` must pass** and new behaviour needs a test, ideally against the real example MCP server rather than mocks.
- Never log or persist request arguments; never put secrets on a command line or in Claude's config.
- Update `CHANGELOG.md` and bump `__version__` in `src/mcp_approval_gate/__init__.py` for releases; tag `vX.Y.Z` to publish.
