# AUR Stable Packaging

Package name: `krunner-spotify-enhanced`

## Release flow

1. Create and push a git tag like `v0.1.0`.
2. Update `pkgver` in `PKGBUILD`.
3. If only packaging changed, increment `pkgrel`.
4. Re-generate `.SRCINFO`:

```bash
cd packaging/aur-stable
makepkg --printsrcinfo > .SRCINFO
```

## Build test locally

```bash
cd packaging/aur-stable
makepkg -si
```

## Notes

- Stable package builds from release tags (`vX.Y.Z`).
- `-git` package tracks upstream `main` and should not be manually version-bumped.
