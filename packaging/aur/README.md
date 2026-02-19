# AUR Packaging

Package name: `krunner-spotify-enhanced-git`

## Files

- `PKGBUILD`
- `.SRCINFO`

## Generate/update `.SRCINFO`

```bash
cd packaging/aur
makepkg --printsrcinfo > .SRCINFO
```

## Build test locally

```bash
cd packaging/aur
makepkg -si
```

## Notes

- Runtime Python dependencies are provided by Arch packages (no bundled venv).
- DBus service and user systemd service run:
  - `/usr/bin/python /usr/lib/krunner-spotify-enhanced/KRunnerSpotify.py`
