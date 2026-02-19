# Troubleshooting

## Plugin appears, but commands do nothing

- Ensure Spotify is running on at least one active device.
- Open KRunner and run `spe login` once to refresh your token.
- Run `./debug.sh` and check for Python exceptions.

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
