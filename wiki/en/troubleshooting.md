# Troubleshooting (EN)

## No results in KRunner

- Run `./install.sh --skip-pip`.
- Restart KRunner (`kquitapp6 krunner`).
- Check user service: `systemctl --user status krunner-spotify.service`.

## Only one autocomplete suggestion for `spe`

- Restart KRunner: `kquitapp6 krunner`.
- Restart runner service: `systemctl --user restart krunner-spotify.service`.
- Type `spe` again in KRunner.

## Spotify API 403

- Open Spotify Developer Dashboard for your app.
- Verify `REDIRECT_URI` matches config (`http://127.0.0.1:3000/callback`).
- Add your account email in **Users and Access**.
- Re-run `spe login`.

## Playback commands do not affect Spotify

- Ensure Spotify is running and an active device exists.
- Re-authenticate with `spe login`.

## Token issues

- Remove cache: `rm -f ~/.cache/KRunnerSpotify/.cache`
- Login again: `spe login`
