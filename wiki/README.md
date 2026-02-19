# Wiki

Diese Wiki-Struktur ist sprachbasiert aufgebaut und leicht erweiterbar.

## Struktur

- `wiki/en/` – English docs
- `wiki/de/` – Deutsche Doku
- `wiki/templates/` – Vorlagen für neue Sprachen

## Neue Sprache hinzufügen

1. Kopiere `wiki/templates/language-index-template.md` nach
   `wiki/<lang>/index.md`.
2. Lege die Seiten `install.md`, `commands.md`, `troubleshooting.md` im selben Ordner an.
3. Verlinke die Sprache in dieser Datei.

## Qualitätsrichtlinien

- Beispiele immer mit `spe` (oder dokumentiertem Alias) schreiben.
- Befehle als kopierbare Blöcke (`bash`/`text`) angeben.
- Pro Sprachordner gleiche Seitennamen beibehalten.
- Änderungen an Befehlsbeispielen mit `make docs-check` verifizieren.

## Verfügbare Sprachen

- [English](en/index.md)
- [Deutsch](de/index.md)
