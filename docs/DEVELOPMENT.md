# Development Guide

## Local setup

1. Clone repository
2. Run `./install.sh`
3. Run plugin directly with `./debug.sh`

## Project structure

- `src/KRunnerSpotify.py`: DBus runner entrypoint
- `src/commands/`: command handlers
- `src/Config.py`: runtime config loader
- `install.sh` / `uninstall.sh`: deployment helpers

## Quality checks

- Python lint/type checks are in GitHub Actions.
- Shell scripts are linted with ShellCheck in CI.

Run locally:

- `make lint`
- `make shellcheck`
- `make docs-check`
- `make test`
- `make smoke`

Optional integration run:

- `make test-integration`

## Manual smoke test flow

1. `./install.sh`
2. Open KRunner
3. Execute:
   - `spe login`
   - `spe play <song>`
   - `spe next`
   - `spe trackinfo`

## Notes for maintainers

- Keep `README.md` and `CREDITS.md` updated when ownership changes.
- Keep this fork attribution clear (GPL and upstream credits).
- Keep AUR metadata in `packaging/aur` and `packaging/aur-stable` in sync.

Regenerate AUR metadata after PKGBUILD updates:

- `cd packaging/aur && makepkg --printsrcinfo > .SRCINFO`
- `cd packaging/aur-stable && makepkg --printsrcinfo > .SRCINFO`
