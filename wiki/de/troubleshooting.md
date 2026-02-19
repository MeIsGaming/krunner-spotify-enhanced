# Fehlerbehebung (DE)

## Keine Treffer in KRunner

- `./install.sh --skip-pip` ausführen.
- KRunner neu starten (`kquitapp6 krunner`).
- User-Service prüfen: `systemctl --user status krunner-spotify.service`.

## Nur ein Autocomplete-Treffer bei `spe`

- KRunner neu starten: `kquitapp6 krunner`.
- Runner-Service neu starten: `systemctl --user restart krunner-spotify.service`.
- Danach `spe` erneut in KRunner eingeben.

## Spotify API 403

- Spotify Developer Dashboard deiner App öffnen.
- Prüfen, ob `REDIRECT_URI` exakt passt (`http://127.0.0.1:3000/callback`).
- Deine Account-Mail unter **Users and Access** hinzufügen.
- Danach `spe login` erneut ausführen.

## Playback-Befehle wirken nicht

- Spotify muss laufen und ein aktives Gerät haben.
- Mit `spe login` neu authentifizieren.

## Token-Probleme

- Cache löschen: `rm -f ~/.cache/KRunnerSpotify/.cache`
- Neu anmelden: `spe login`
