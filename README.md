# KRunner SpotifyEnhanced

Control [Spotify](https://www.spotify.com/) directly from
[KRunner](https://github.com/KDE/krunner) using `spe` commands.

## Highlights

- Universal playback control across Spotify devices
- Command prefix flow (`spe play`, `spe next`, `spe pause`, ...)
- Search for songs, artists, playlists, podcasts, episodes
- Queue management, seek, repeat, shuffle, volume, track info
- Fork-maintained by Ashley (MeIsGaming) with upstream credits retained

## Requirements

- Linux with KDE Plasma / KRunner
- Python 3.9+
- `python3-venv`
- `pip`

## Install

```sh
git clone https://github.com/MeIsGaming/krunner-spotify.git
cd krunner-spotify
./install.sh
```

Optional install flags:

```sh
./install.sh --no-restart
./install.sh --python python3.12
./install.sh --skip-pip
./install.sh --no-systemd
```

Installer actions:

- Creates `.venv` (if missing)
- Installs Python dependencies
- Installs KRunner DBus plugin metadata
- Installs and starts a user `systemd` service (`krunner-spotify.service`) when available
- Installs icons into `~/.local/share/pixmaps`
- Restarts KRunner if `kquitapp6` is available

## Verify Installation

After install, check these files exist:

- `~/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop`
- `~/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service`
- `~/.config/KRunner-Spotify/KRunner-Spotify.config`

Then open KRunner and run:

```text
spe login
spe trackinfo
```

## Quick Usage

```text
spe
spe login
spe play bohemian rhapsody
spe next
spe pause
spe resume
```

Full command reference: [USAGE.md](USAGE.md)

## Compatibility

- Primary command prefix is `spe`.
- Optional legacy alias mode (`sp`) can be enabled in config:

```ini
ENABLE_LEGACY_SP_ALIAS = True
```

Config file path:

- `~/.config/KRunner-Spotify/KRunner-Spotify.config`

## Common Fixes

- If only one suggestion appears when typing `spe`, restart KRunner and service:

```sh
kquitapp6 krunner
systemctl --user restart krunner-spotify.service
```

- If commands still show `403`, verify `CLIENT_ID`, `REDIRECT_URI`, and app user access in Spotify Dashboard.

## Quality & Tests

```sh
make lint
make shellcheck
make docs-check
make test
make smoke
```

Optional integration tests (requires running DBus service):

```sh
make test-integration
```

## Debug / Uninstall

```sh
./debug.sh
./uninstall.sh
```

Additional options:

```sh
./debug.sh --no-redeploy
./uninstall.sh --keep-config --keep-cache
```

If KRunner does not auto-activate the DBus service on your distro/session bus,
the user `systemd` service keeps the runner available in the background.

## Documentation

- [wiki/README.md](wiki/README.md): multilingual wiki entrypoint (DE/EN, extensible)
- [USAGE.md](USAGE.md): command reference
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): local dev guide
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): common issues
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution rules
- [CREDITS.md](CREDITS.md): attribution and maintainer info
- [CHANGELOG.md](CHANGELOG.md): release notes
- [packaging/aur](packaging/aur): AUR `-git` package files (builds from upstream `main`)
- [packaging/aur-stable](packaging/aur-stable): AUR stable package files

## Maintainer

- Ashley (MeIsGaming)
- Contact: <mailto:info@meisgaming.net>

## Credits

This repository is a maintained fork and keeps clear attribution:

- Original project author: Martijn Vogelaar
- Maintained/extended by: Jochem Kuipers
- Current fork maintainer: Ashley (MeIsGaming)
- Upstream: <https://github.com/JochemKuipers/krunner-spotify>

## License

Distributed under GPL-3.0. See `LICENSE`.
