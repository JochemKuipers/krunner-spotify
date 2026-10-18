from Config import getCommandName

from .Command import Command


class Previous(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PREVIOUS_COMMAND"), spotify)

    def Match(self, query: str):
        return [(self.command, "Play previous track", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        self.spotify.previous_track()
