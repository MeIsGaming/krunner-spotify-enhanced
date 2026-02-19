#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(realpath "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"
REDEPLOY=1

usage() {
    cat <<'EOF'
Usage: ./debug.sh [options]

Options:
  --no-redeploy   Do not rewrite service/desktop files before start
  -h, --help      Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-redeploy)
            REDEPLOY=0
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

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Run ./install.sh first."
    exit 1
fi

if command -v systemctl >/dev/null 2>&1; then
    systemctl --user stop krunner-spotify.service 2>/dev/null || true
fi

if [[ "$REDEPLOY" -eq 1 ]]; then
    mkdir -p "$HOME/.local/share/krunner/dbusplugins"
    mkdir -p "$HOME/.local/share/dbus-1/services"
    install -m 0644 "$PROJECT_DIR/plasma-runner-KRunnerSpotify.desktop" "$HOME/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop"
    sed -e "s|%{PROJECTDIR}|$PROJECT_DIR|g" "$PROJECT_DIR/org.kde.KRunnerSpotify.service" > "$HOME/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service"
fi

echo "Stopping existing KRunner and plugin processes..."
pkill -9 -f KRunnerSpotify.py 2>/dev/null || true
if command -v kquitapp6 >/dev/null 2>&1; then
    kquitapp6 krunner 2>/dev/null || true
fi
sleep 1

echo "Starting KRunner SpotifyEnhanced in debug mode..."
echo "Press Ctrl+C to stop."
"$VENV_DIR/bin/python" "$PROJECT_DIR/src/KRunnerSpotify.py"