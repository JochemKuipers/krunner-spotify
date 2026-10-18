from Config import getCommandName
from Util import parse_duration_seconds

from .Command import Command


class Seek(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("SEEK_COMMAND"), spotify)

    def Match(self, query: str):
        seconds = parse_duration_seconds(query)
        if seconds is None:
            return [("", "Invalid input.", "Spotify", 100, 100, {})]
        raw = query.strip(" ")
        parts = raw.split(":")
        if len(parts) == 1:
            desc = f"Seek: {parts[0]} sec"
        elif len(parts) == 2:
            desc = f"Seek: {parts[0]} min {parts[1]} sec"
        else:
            desc = f"Seek: {parts[0]} hr {parts[1]} min {parts[2]} sec"
        return [(self.command + " " + str(seconds), desc, "Spotify", 100, 100, {})]

    def Run(self, data: str):
        self.spotify.seek_track(int(data) * 1000)
