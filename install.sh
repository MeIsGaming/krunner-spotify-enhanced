#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(realpath "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SKIP_PIP=0
RESTART_KRUNNER=1
USE_SYSTEMD=1

usage() {
    cat <<'EOF'
Usage: ./install.sh [options]

Options:
  --python <bin>    Python binary to use (default: python3)
  --skip-pip        Skip dependency installation step
  --no-restart      Do not restart KRunner after install
    --no-systemd      Do not install/start user systemd service
  -h, --help        Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --python)
            [[ $# -lt 2 ]] && { echo "Error: --python requires an argument"; exit 1; }
            PYTHON_BIN="$2"
            shift 2
            ;;
        --skip-pip)
            SKIP_PIP=1
            shift
            ;;
        --no-restart)
            RESTART_KRUNNER=0
            shift
            ;;
        --no-systemd)
            USE_SYSTEMD=0
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

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Error: '$PYTHON_BIN' is not available. Install Python 3 first."
    exit 1
fi

required_files=(
    "$PROJECT_DIR/requirements.txt"
    "$PROJECT_DIR/plasma-runner-KRunnerSpotify.desktop"
    "$PROJECT_DIR/org.kde.KRunnerSpotify.service"
    "$PROJECT_DIR/krunner-spotify.systemd.service"
    "$PROJECT_DIR/KRunner-Spotify.config"
)

for file_path in "${required_files[@]}"; do
    if [[ ! -f "$file_path" ]]; then
        echo "Error: Required file missing: $file_path"
        exit 1
    fi
done

echo "Installing KRunner SpotifyEnhanced from: $PROJECT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

if [[ "$SKIP_PIP" -eq 0 ]]; then
    echo "Installing Python dependencies..."
    "$VENV_DIR/bin/python" -m pip install --upgrade pip
    "$VENV_DIR/bin/python" -m pip install -r "$PROJECT_DIR/requirements.txt"
else
    echo "Skipping dependency installation (--skip-pip)."
fi

mkdir -p "$HOME/.local/share/krunner/dbusplugins"
mkdir -p "$HOME/.local/share/dbus-1/services"
mkdir -p "$HOME/.config/KRunner-Spotify"
mkdir -p "$HOME/.local/share/pixmaps"

install -m 0644 "$PROJECT_DIR/KRunner-Spotify.config" "$HOME/.config/KRunner-Spotify/KRunner-Spotify.config"
install -m 0644 "$PROJECT_DIR/plasma-runner-KRunnerSpotify.desktop" "$HOME/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop"

for icon_file in "$PROJECT_DIR"/icons/*.svg; do
    install -m 0644 "$icon_file" "$HOME/.local/share/pixmaps/$(basename "$icon_file")"
done

sed -e "s|%{PROJECTDIR}|$PROJECT_DIR|g" "$PROJECT_DIR/org.kde.KRunnerSpotify.service" > "$HOME/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service"

if [[ "$USE_SYSTEMD" -eq 1 ]]; then
    mkdir -p "$HOME/.config/systemd/user"
    sed -e "s|%{PROJECTDIR}|$PROJECT_DIR|g" "$PROJECT_DIR/krunner-spotify.systemd.service" > "$HOME/.config/systemd/user/krunner-spotify.service"

    if command -v systemctl >/dev/null 2>&1; then
        systemctl --user daemon-reload || true
        systemctl --user enable --now krunner-spotify.service || true
        systemctl --user restart krunner-spotify.service || true
    fi
fi

if [[ "$RESTART_KRUNNER" -eq 1 ]] && command -v kquitapp6 >/dev/null 2>&1; then
    kquitapp6 krunner 2>/dev/null || true
fi

echo "Installation complete."