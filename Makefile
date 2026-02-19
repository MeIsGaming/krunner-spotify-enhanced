.PHONY: install install-no-restart uninstall debug lint shellcheck verify-install service-status service-restart smoke

install:
	./install.sh

install-no-restart:
	./install.sh --no-restart

uninstall:
	./uninstall.sh

debug:
	./debug.sh

lint:
	@if [ -x .venv/bin/ruff ]; then .venv/bin/ruff check src; else echo "ruff not installed in .venv"; fi
	@if [ -x .venv/bin/pyright ]; then .venv/bin/pyright; else echo "pyright not installed in .venv"; fi

shellcheck:
	@if command -v shellcheck >/dev/null 2>&1; then \
		shellcheck -x -S warning install.sh uninstall.sh debug.sh; \
	elif [ -x .venv/bin/shellcheck ]; then \
		.venv/bin/shellcheck -x -S warning install.sh uninstall.sh debug.sh; \
	else \
		echo "shellcheck not installed (system or .venv/bin/shellcheck)"; \
		exit 1; \
	fi

verify-install:
	ls -l $(HOME)/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop
	ls -l $(HOME)/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service
	ls -l $(HOME)/.config/KRunner-Spotify/KRunner-Spotify.config

service-status:
	@systemctl --user status krunner-spotify.service --no-pager || true

service-restart:
	@systemctl --user restart krunner-spotify.service

smoke:
	@dbus-send --session --print-reply --dest=org.kde.KRunnerSpotify /KRunnerSpotify org.kde.krunner1.Match string:'spe login' >/dev/null
	@echo "Smoke test OK"
