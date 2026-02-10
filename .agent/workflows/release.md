---
description: How to create a new release of notebooklm-mcp-cli
---

# Release Process

// turbo-all

## Steps

1. Ensure you're on the release branch (e.g., `dev/0.2.18`)

2. Bump version in both files:
   - `pyproject.toml` → `version = "X.Y.Z"`
   - `src/notebooklm_tools/__init__.py` → `__version__ = "X.Y.Z"`

3. Update `CHANGELOG.md` with the new version entry

4. Rebuild the MCPB extension package (auto-syncs version from pyproject.toml):
```bash
python3 scripts/build_mcpb.py
```

5. Reinstall locally and test:
```bash
uv cache clean && uv tool install --force .
```

6. Run tests:
```bash
uv run pytest
```

7. Commit all changes:
```bash
git add -A && git commit -m "release: vX.Y.Z"
```

8. Merge to main and tag:
```bash
git checkout main && git merge dev/X.Y.Z
git tag vX.Y.Z && git push origin main --tags
```

9. Publish to PyPI:
```bash
uv build && uv publish
```

## Checklist

- [ ] Version bumped in `pyproject.toml` and `__init__.py`
- [ ] CHANGELOG updated
- [ ] MCPB rebuilt (`python3 scripts/build_mcpb.py`)
- [ ] Tests pass
- [ ] Committed and pushed
- [ ] Tagged
- [ ] Published to PyPI
