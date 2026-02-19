# Project TODOs

## Recently Completed

- [x] DBus integration tests for `Match` and `Run`.
- [x] Optional legacy alias mode (`sp` -> `spe`).
- [x] Command metadata unit tests (autocomplete/registry sync).
- [x] AUR stable package scaffold next to `-git` package.
- [x] Localized docs consistency checks in CI.

## Next Priorities

- [ ] Add pytest coverage report export in CI (`--cov=src --cov-report=xml`).
- [ ] Add negative tests for malformed queries (`spe`, `spe-empty`, invalid seek inputs).
- [ ] Add command permission diagnostics page for Spotify dashboard setup.
- [ ] Add release checklist (`tag`, changelog update, AUR stable sync).
- [ ] Add optional command aliases per command (`PAUSE_ALIASES = stop,halt`).
- [ ] Add resilient fallback for unavailable config editor binary.
- [ ] Introduce typed result alias for KRunner tuple shape.
- [ ] Add lightweight benchmark script for autocomplete latency.
