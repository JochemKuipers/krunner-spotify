#!/bin/sh

# Exit if something fails
set -e

print_dep_help() {
    echo ""
    echo "Missing native Python bindings (dbus / PyGObject)."
    echo "Prefer distro packages (no compile):"
    echo "  Debian/Ubuntu/PikaOS:  sudo apt install python3-gi python3-dbus"
    echo "  Fedora:                sudo dnf install python3-gobject python3-dbus"
    echo "  Arch:                  sudo pacman -S python-gobject python-dbus"
    echo "  openSUSE:              sudo zypper install python3-gobject python3-dbus-python"
    echo ""
    echo "Or install build dependencies so pip can compile them:"
    echo "  Debian/Ubuntu/PikaOS:  sudo apt install gcc pkg-config python3-dev libcairo2-dev libgirepository-2.0-dev libdbus-1-dev"
    echo "  Fedora:                sudo dnf install gcc pkg-config python3-devel cairo-gobject-devel gobject-introspection-devel dbus-devel"
    echo "  Arch:                  sudo pacman -S cairo pkgconf gobject-introspection"
    echo "  openSUSE:              sudo zypper install gcc pkg-config python3-devel cairo-devel gobject-introspection-devel dbus-1-devel"
}

has_gi_pkgconfig() {
    pkg-config --exists gobject-introspection-1.0 2>/dev/null \
        || pkg-config --exists girepository-2.0 2>/dev/null
}

check_build_deps() {
    missing=""
    if ! command -v pkg-config >/dev/null 2>&1; then
        missing="pkg-config"
    else
        pkg-config --exists cairo 2>/dev/null || missing="$missing cairo"
        has_gi_pkgconfig || missing="$missing gobject-introspection-1.0/girepository-2.0"
        pkg-config --exists dbus-1 2>/dev/null || missing="$missing dbus-1"
        # trim leading space
        missing=$(echo "$missing" | sed 's/^ *//')
    fi
    if [ -n "$missing" ]; then
        echo "Missing build dependencies: $missing"
        return 1
    fi
    return 0
}

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv --system-site-packages .venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
. .venv/bin/activate
pip install --upgrade pip

if ! python -c "import dbus; from gi.repository import GLib" 2>/dev/null; then
    if grep -q '^include-system-site-packages = false$' .venv/pyvenv.cfg 2>/dev/null; then
        echo "Existing .venv cannot see system packages (include-system-site-packages = false)."
        echo "Install runtime packages (see below), then recreate the venv:"
        echo "  rm -rf .venv && sh install.sh"
        print_dep_help
        deactivate
        exit 1
    fi

    echo "System dbus/PyGObject not found; checking build dependencies for pip install..."
    if check_build_deps; then
        pip install dbus-python PyGObject
    else
        print_dep_help
        deactivate
        exit 1
    fi

    if ! python -c "import dbus; from gi.repository import GLib" 2>/dev/null; then
        echo "dbus/PyGObject still not importable after install."
        print_dep_help
        deactivate
        exit 1
    fi
fi

pip install -r requirements.txt
deactivate

mkdir -p ~/.local/share/krunner/dbusplugins/
mkdir -p ~/.local/share/dbus-1/services/
mkdir -p ~/.config/KRunner-Spotify
mkdir -p ~/.local/share/pixmaps
cp icons/* ~/.local/share/pixmaps

cp KRunner-Spotify.config ~/.config/KRunner-Spotify/
cp plasma-runner-KRunnerSpotify.desktop ~/.local/share/krunner/dbusplugins/
sed -e "s|%{PROJECTDIR}|${PWD}|g" "org.kde.KRunnerSpotify.service" > ~/.local/share/dbus-1/services/org.kde.KRunnerSpotify.service

# dbus-broker only loads new ~/.local/share/dbus-1/services/ files after reload
if systemctl --user is-active dbus-broker.service >/dev/null 2>&1; then
    systemctl --user reload dbus-broker.service
fi

pkill -f KRunnerSpotify.py 2>/dev/null || true
kquitapp6 krunner 2>/dev/null || true
