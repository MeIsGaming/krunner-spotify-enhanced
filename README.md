# KRunner SpotifyEnhanced

Control [Spotify](https://www.spotify.com/) directly from [KRunner](https://github.com/KDE/krunner) using `spe` commands.

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
spe login
spe play bohemian rhapsody
spe next
spe pause
spe resume
```

Full command reference: [USAGE.md](USAGE.md)

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

- [USAGE.md](USAGE.md): command reference
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): local dev guide
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md): common issues
- [CONTRIBUTING.md](CONTRIBUTING.md): contribution rules
- [CREDITS.md](CREDITS.md): attribution and maintainer info
- [CHANGELOG.md](CHANGELOG.md): release notes

## Maintainer

- Ashley (MeIsGaming)
- Contact: info@meisgaming.net

## Credits

This repository is a maintained fork and keeps clear attribution:

- Original project author: Martijn Vogelaar
- Maintained/extended by: Jochem Kuipers
- Current fork maintainer: Ashley (MeIsGaming)
- Upstream: https://github.com/JochemKuipers/krunner-spotify

## License

Distributed under GPL-3.0. See `LICENSE`.
