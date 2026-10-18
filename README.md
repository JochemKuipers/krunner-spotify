# KRunner-Spotify

Control [Spotify](https://www.spotify.com/) directly from [KRunner](https://github.com/KDE/krunner) using simple commands prefixed with `sp`. This plugin uses [Spotipy](https://github.com/plamere/spotipy) to interact with the [Spotify Web API](https://developer.spotify.com/documentation/web-api/), allowing you to control Spotify playback on any device - your phone, Chromecast, Smart TV, or computer - all from your KDE desktop.

## Features

* **Universal Control**: Control Spotify on any device connected to your account
* **Prefix-based Commands**: All commands start with `sp` for easy access (e.g., `sp play`, `sp next`)
* **Rich Functionality**: Play songs, control playback, manage playlists, adjust volume, and more
* **Search Integration**: Search for songs, artists, playlists, podcasts, and episodes
* **Queue Management**: Add tracks to your queue on the fly

## Dependencies

* [Python 3](https://www.python.org/download/releases/3.0/)
* [Pip 3](https://pip.pypa.io/en/stable/)
* [Spotipy](https://spotipy.readthedocs.io/) (minimum version 2.14.0) — installed into the project venv by `install.sh`
* Native bindings for D-Bus and GLib (prefer distro packages; PyGObject has no Linux wheels on PyPI):
  * Debian/Ubuntu/PikaOS: `python3-gi python3-dbus`
  * Fedora: `python3-gobject python3-dbus`
  * Arch: `python-gobject python-dbus`
  * openSUSE: `python3-gobject python3-dbus-python`
* KDE Plasma with KRunner

If those runtime packages are missing, `install.sh` checks for build headers and can compile `dbus-python` / `PyGObject` from pip instead. On Debian/Ubuntu/PikaOS that means:

```sh
sudo apt install gcc pkg-config python3-dev libcairo2-dev libgirepository-2.0-dev libdbus-1-dev
```

The installer exits early with package suggestions if neither path is available, instead of failing deep inside Meson.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/JochemKuipers/krunner-spotify
cd krunner-spotify
```

2. Install runtime packages (recommended), then run the install script:

```sh
# Debian/Ubuntu/PikaOS example
sudo apt install python3-gi python3-dbus

sh install.sh
```

The installer creates a virtual environment with access to system site-packages, uses distro `dbus` / `gi` when present, and installs Spotipy automatically.

3. **Configure KRunner Priority (Recommended)**:
   * Open KRunner settings (search for "KRunner" in System Settings)
   * Go to the "Plugins" section
   * Find "KRunner Spotify" in the list
   * Add it to your **Favorites** and move it to the **top** of the favorites list
   * This ensures Spotify results always appear first when using the `sp` prefix

## Spotify Developer Setup

> [!IMPORTANT]
> Required before first use. The plugin needs a Spotify Developer app to authenticate with the Spotify Web API.

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in
2. Click **Create app**
3. Fill in any name/description, then under **Redirect URIs** add:
   ```
   http://127.0.0.1:3000/callback
   ```
4. Under **APIs used**, select **Web API**
5. Save the app, open its settings, and copy the **Client ID**
6. Paste it into `~/.config/KRunner-Spotify/KRunner-Spotify.config` under `[Settings]`:
   ```ini
   CLIENT_ID = your_client_id_here
   ```

> [!NOTE]
> **As of February 2026**, Spotify limits developers to 1 app in development mode. If you already have an existing Spotify app (e.g. for Home Assistant), you can reuse it — just add your loopback callback URL as an additional Redirect URI rather than creating a new app.

## Uninstall

Navigate to the repository directory and run:

```sh
sh uninstall.sh
```

## Quick Start

All commands must be prefixed with `sp` (e.g., `sp login`, `sp play Bohemian Rhapsody`).

1. First time setup - authenticate with Spotify:

``` krunner
sp login
```

2. Play music:

``` krunner
sp play <track name>
sp song <search query>
sp artist <artist name>
sp playlist <playlist name>
```

## Debugging

To run the plugin in debug mode and see console output:
```sh
sh debug.sh
```

## Configuration

The configuration file is located at `~/.config/KRunner-Spotify/KRunner-Spotify.config`. You can edit it directly or use:

``` krunner
sp editconfig
```

## Troubleshooting

**Plugin results have low priority:**

* Open KRunner settings in System Settings
* Add "KRunner Spotify" to Favorites
* Move it to the top of the favorites list
* This ensures `sp` commands always show results first

**Plugin not appearing:**

On systems using **dbus-broker** (common on Arch and CachyOS), newly installed D-Bus service files are not picked up until the broker is reloaded or you log out and back in:

```sh
systemctl --user reload dbus-broker.service
pkill -9 -f KRunnerSpotify.py
kquitapp6 krunner
```

Then open KRunner again and try a command such as `sp play`.

**Note:** `debug.sh` runs the plugin directly in the foreground; that bypasses D-Bus activation. After you stop it, KRunner relies on D-Bus to start the plugin on demand — which only works if the service file is registered (see above).

## License

Distributed under the GPL-3.0 License. See [`LICENSE`](LICENSE) for more information.

## Credits

Original project by Martijn Vogelaar  
Maintained and updated by Jochem Kuipers

Project Link: [GitHub](https://github.com/JochemKuipers/krunner-spotify)

* **Playback Control**: Play, pause, resume, next, previous, shuffle, repeat
* **Search & Play**: Songs, artists, playlists, podcasts, episodes
* **Queue Management**: Add tracks to queue
* **Volume Control**: Increase, decrease, or set specific volume levels
* **Track Information**: View current track details
* **Advanced**: Fast forward, rewind, seek to specific time
* **Configuration**: Edit config, reload settings, login/logout

## Future implementations

* Control your own playlists
  * Create
  * Delete
  * Rename
  * Add (current) song to playlist
* Search and play album by name
* Search and play album by artists name
* Play an artist besides just searching for songs by artist.

## License

Distributed under the GPL-3.0 License. See [`LICENSE`](LICENSE) for more information.

## Contact

Martijn Vogelaar - <jochem@kuipers.cc>

Project Link: [GitHub](https://github.com/JochemKuipers/krunner-spotify)
