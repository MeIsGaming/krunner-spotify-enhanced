# Release (EN)

## Suggested release flow

1. Update `CHANGELOG.md`.
2. Run full local checks.
3. Create git tag (`vX.Y.Z`).
4. Update stable AUR metadata in `packaging/aur-stable`.
5. Re-generate `.SRCINFO` for stable and `-git` packages.

## Commands

```bash
make lint && make shellcheck && make docs-check && make test && make smoke
```
