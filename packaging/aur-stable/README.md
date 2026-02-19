# AUR Stable Packaging

Package name: `krunner-spotify-enhanced`

## Release flow

1. Create and push a git tag like `v0.1.0`.
2. Update `pkgver` in `PKGBUILD`.
3. Re-generate `.SRCINFO`:

```bash
cd packaging/aur-stable
makepkg --printsrcinfo > .SRCINFO
```

## Build test locally

```bash
cd packaging/aur-stable
makepkg -si
```
