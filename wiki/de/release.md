# Release (DE)

## Empfohlener Release-Ablauf

1. `CHANGELOG.md` aktualisieren.
2. Vollständige lokale Checks ausführen.
3. Git-Tag erstellen (`vX.Y.Z`).
4. Stable-AUR-Metadaten in `packaging/aur-stable` aktualisieren (`pkgver`; bei Packaging-only Änderungen `pkgrel` erhöhen).
5. `packaging/aur` als upstream-tracking `-git` Paket beibehalten (kein manuelles `pkgver`-Bumping).
6. `.SRCINFO` für stable und `-git` neu erzeugen.

## Kommando

```bash
make lint && make shellcheck && make docs-check && make test && make smoke
```
