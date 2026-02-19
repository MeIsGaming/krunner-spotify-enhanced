# Testing (EN)

Run all quality checks locally:

```bash
make lint
make shellcheck
make docs-check
make test
make test-integration
make smoke
```

## Notes

- `test-integration` requires a working session DBus and runner service.
- `docs-check` validates required examples in localized command pages.
