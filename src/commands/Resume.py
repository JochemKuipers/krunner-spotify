from Config import getCommandName

from .Command import Command


class Resume(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("RESUME_COMMAND"), spotify)

    def Match(self, query: str):
        return [(self.command, "Start/Resume current song", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        self.spotify.start_playback()
