# Release (DE)

## Empfohlener Release-Ablauf

1. `CHANGELOG.md` aktualisieren.
2. Vollständige lokale Checks ausführen.
3. Git-Tag erstellen (`vX.Y.Z`).
4. Stable-AUR-Metadaten in `packaging/aur-stable` aktualisieren.
5. `.SRCINFO` für stable und `-git` neu erzeugen.

## Kommando

```bash
make lint && make shellcheck && make docs-check && make test && make smoke
```
