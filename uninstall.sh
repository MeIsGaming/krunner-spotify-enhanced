#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(realpath "$SCRIPT_DIR")"
KEEP_CONFIG=0
KEEP_CACHE=0
RESTART_KRUNNER=1

usage() {
	cat <<'EOF'
Usage: ./uninstall.sh [options]

Options:
  --keep-config   Keep ~/.config/KRunner-Spotify
  --keep-cache    Keep ~/.cache/KRunnerSpotify
  --no-restart    Do not restart KRunner
  -h, --help      Show this help
EOF
}

while [[ $# -gt 0 ]]; do
	case "$1" in
		--keep-config)
			KEEP_CONFIG=1
			shift
			;;
		--keep-cache)
			KEEP_CACHE=1
			shift
			;;
		--no-restart)
			RESTART_KRUNNER=0
			shift
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "Error: Unknown option: $1"
			usage
			exit 1
			;;
	esac
done

pkill -9 -f KRunnerSpotify.py 2>/dev/null || true

if command -v systemctl >/dev/null 2>&1; then
	systemctl --user disable --now krunner-spotify.service 2>/dev/null || true
	systemctl --user daemon-reload 2>/dev/null || true
fi
rm -f "$HOME/.config/systemd/user/krunner-spotify.service"

rm -f "$HOME/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop"
rm -f "$HOME/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service"

if [[ "$KEEP_CONFIG" -eq 0 ]]; then
    rm -rf "$HOME/.config/KRunner-Spotify"
fi

for icon_file in "$PROJECT_DIR"/icons/*.svg; do
	rm -f "$HOME/.local/share/pixmaps/$(basename "$icon_file")"
done

if [[ "$KEEP_CACHE" -eq 0 ]]; then
    rm -rf "$HOME/.cache/KRunnerSpotify"
fi

if [[ "$RESTART_KRUNNER" -eq 1 ]] && command -v kquitapp6 >/dev/null 2>&1; then
	kquitapp6 krunner 2>/dev/null || true
fi

echo "KRunner SpotifyEnhanced uninstalled successfully."