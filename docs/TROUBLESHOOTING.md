# Troubleshooting

## Plugin appears, but commands do nothing

- Ensure Spotify is running on at least one active device.
- Open KRunner and run `spe login` once to refresh your token.
- Run `./debug.sh` and check for Python exceptions.

## `spe list` / `spe help` only shows ~10 entries

- The runner can return many commands, but KRunner UI may show only a limited amount at once.
- Use paging commands:
  - `spe list 2`
  - `spe list 3`
  - `spe list next`
  - `spe list prev`
- Use filtered discovery for faster selection:
  - `spe list vol`
  - `spe help play`

## Spotify API 403 (commands appear but do nothing)

- If KRunner shows `Spotify API denied request (403)`, your account is likely not allowed for your Spotify app.
- Open Spotify Developer Dashboard and go to your app.
- Add your Spotify account email under **Users and Access**.
- Ensure the app is in the correct mode for your account access.
- Then run:
  - `spe login`
  - `spe trackinfo`

## Plugin does not appear in KRunner

- Reinstall service files:
  - `./install.sh`
- Restart KRunner:
  - `kquitapp6 krunner`
- Confirm service file exists:
  - `~/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service`

## Login loop or auth problems

- Remove cached token and login again:
  - `rm -f ~/.cache/KRunnerSpotify/.cache`
  - `spe login`
- Verify `CLIENT_ID` and `REDIRECT_URI` in:
  - `~/.config/KRunner-Spotify/KRunner-Spotify.config`

## Missing Python dependencies

- Ensure system packages are available (`python3-venv`, `pip`).
- Recreate virtual environment:
  - `rm -rf .venv && ./install.sh`

## Icons are missing

- Re-run installer to copy SVG icons into local pixmaps:
  - `./install.sh`
- Confirm files exist in:
  - `~/.local/share/pixmaps`
