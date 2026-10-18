#!/bin/sh
set -e

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run install.sh first."
    exit 1
fi

# Seed config if missing (do not overwrite an existing one)
if [ ! -f "$HOME/.config/KRunner-Spotify/KRunner-Spotify.config" ]; then
    mkdir -p "$HOME/.config/KRunner-Spotify"
    cp KRunner-Spotify.config "$HOME/.config/KRunner-Spotify/"
fi

echo "Stopping existing KRunner and plugin processes..."
pkill -9 -f KRunnerSpotify.py 2>/dev/null || true
kquitapp6 krunner 2>/dev/null || true
sleep 1

echo "Starting KRunner Spotify in debug mode..."
echo "Press Ctrl+C to stop."
. .venv/bin/activate
python3 src/KRunnerSpotify.py
