# Troubleshooting (EN)

## No results in KRunner

- Run `./install.sh --skip-pip`.
- Restart KRunner (`kquitapp6 krunner`).
- Check user service: `systemctl --user status krunner-spotify.service`.

## Playback commands do not affect Spotify

- Ensure Spotify is running and an active device exists.
- Re-authenticate with `spe login`.

## Token issues

- Remove cache: `rm -f ~/.cache/KRunnerSpotify/.cache`
- Login again: `spe login`
