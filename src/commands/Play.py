from Config import getCommandName, getSetting
from Util import handle_spotify_uri

from .Command import Command
from .registry import PLAY_KEYS, resolve


class Play(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_COMMAND"), spotify)

    def Match(self, query: str):
        if " " in query:
            command, arguments = query.split(" ", 1)
        else:
            command, arguments = query, ""

        try:
            if getSetting("CASE_SENSITIVE") == "False":
                command = command.upper()
            results = resolve(command, self.spotify, PLAY_KEYS).Match(arguments)
            for i in range(len(results)):
                row = list(results[i])
                row[0] = self.command + " " + row[0]
                results[i] = tuple(row)
            return results
        except RuntimeError:
            return [("", "Invalid command", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        handle_spotify_uri(self.spotify, data)
