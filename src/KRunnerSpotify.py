import os
import sys

# Add the src directory to Python path so imports work when run via D-Bus
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import dbus.service
import spotipy
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from spotipy.oauth2 import SpotifyPKCE

from commands import Commands
from Config import getCommandName, getSetting
from Util import handle_spotify_uri

DBusGMainLoop(set_as_default=True)

objpath = "/KRunnerSpotify"
iface1 = "org.kde.krunner1"
iface2 = "org.kde.krunner2"


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(
            self,
            dbus.service.BusName("org.kde.KRunnerSpotify", dbus.SessionBus()),
            objpath,
        )
        os.makedirs(os.path.dirname(getSetting("CACHE_PATH")), exist_ok=True)
        self.auth_manager = SpotifyPKCE(
            client_id=getSetting("CLIENT_ID"),
            cache_path=getSetting("CACHE_PATH"),
            redirect_uri=getSetting("REDIRECT_URI"),
            scope=getSetting("ACCES_SCOPE"),
        )
        self.spotify = spotipy.Spotify(auth_manager=self.auth_manager)

    def _match_impl(self, query: str):
        # Check if query starts with "sp " prefix
        if not query.lower().startswith("sp "):
            return []

        # Remove "sp " prefix
        query = query[3:]

        arguments = ""
        if " " in query:
            command, arguments = query.split(" ", 1)
        else:
            command = query
        try:
            if getSetting("CASE_SENSITIVE") == "False":
                command = command.upper()
            return Commands.executeCommand(command, self.spotify).Match(arguments) or []
        except RuntimeError as e:
            if str(e) == "Not logged in!":
                return [
                    (
                        getCommandName("LOGIN_COMMAND"),
                        "Not logged in, click to login",
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            return []

    def _run_impl(self, data: str, action_id: str):
        # If data is a Spotify URI (from search results), handle it directly
        if data.startswith("spotify:"):
            handle_spotify_uri(self.spotify, data)
            return

        # Otherwise, treat as a command - remove "sp " prefix if present
        if data.lower().startswith("sp "):
            data = data[3:]

        command = data
        if " " in data:
            command, data = data.split(" ", 1)
        else:
            data = ""
        try:
            Commands.executeCommand(command, self.spotify).Run(data)
        except RuntimeError as e:
            print(e)

    # Support both krunner1 (Plasma 6) and krunner2 (Plasma 5) interfaces
    @dbus.service.method(iface1, in_signature="s", out_signature="a(sssida{sv})")
    @dbus.service.method(iface2, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):
        return self._match_impl(query)

    @dbus.service.method(iface1, in_signature="ss")
    @dbus.service.method(iface2, in_signature="ss")
    def Run(self, data: str, action_id: str):
        self._run_impl(data, action_id)


runner = Runner()
loop = GLib.MainLoop()
loop.run()
