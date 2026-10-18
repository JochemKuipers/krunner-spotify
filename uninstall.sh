
#!/bin/bash

# Exit if something fails
set -e

# Kill the KRunner Spotify process
pkill -9 -f KRunnerSpotify.py || true

# Remove files
rm -f ~/.local/share/krunner/dbusplugins/plasma-runner-KRunnerSpotify.desktop
rm -f ~/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service
rm -f ~/.config/KRunner-Spotify/KRunner-Spotify.config
rm -rf ~/.config/KRunner-Spotify

# Delete icons
rm -f ~/.local/share/pixmaps/Spotify.svg

# Deletes cache from the default CACHE_PATH, has to be manually deleted if changed
rm -f ~/.cache/KRunnerSpotify/.cache
rm -rf ~/.cache/KRunnerSpotify

# Restart KRunner
kquitapp6 krunner 2>/dev/null || true

echo "KRunner Spotify uninstalled successfully!"