# Tests (DE)

Alle Qualitätschecks lokal ausführen:

```bash
make lint
make shellcheck
make docs-check
make test
make test-integration
make smoke
```

## Hinweise

- `test-integration` benötigt eine funktionierende Session-DBus-Umgebung.
- `docs-check` validiert verpflichtende Beispiele in lokalisierten Command-Seiten.
