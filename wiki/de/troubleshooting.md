# Fehlerbehebung (DE)

## Keine Treffer in KRunner

- `./install.sh --skip-pip` ausführen.
- KRunner neu starten (`kquitapp6 krunner`).
- User-Service prüfen: `systemctl --user status krunner-spotify.service`.

## Playback-Befehle wirken nicht

- Spotify muss laufen und ein aktives Gerät haben.
- Mit `spe login` neu authentifizieren.

## Token-Probleme

- Cache löschen: `rm -f ~/.cache/KRunnerSpotify/.cache`
- Neu anmelden: `spe login`
