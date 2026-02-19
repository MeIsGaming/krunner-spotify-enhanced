# Changelog

## Unreleased

### Enhancements

- Installer no longer depends on shell `$PWD`; it resolves project path canonically.
- Installer gained flags: `--python`, `--skip-pip`, `--no-restart`.
- Installer now validates required files before deployment.
- Debug script gained `--no-redeploy` option.
- Uninstaller gained `--keep-config`, `--keep-cache`, `--no-restart`.
- Command dispatch was refactored to dictionary-based lookup.
- Runner logging improved with `KRUNNER_SPOTIFY_LOG_LEVEL`.
- Runtime exception handling in the runner is now safer and less noisy.
- Config editor launch switched from shell invocation to `subprocess.Popen`.
- Added `Makefile` helper commands for install/debug/lint/verify.
