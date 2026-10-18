import os

from Config import getSetting


class Command:
    def __init__(self, command, spotify):
        self.spotify = spotify
        self.command = command
        if not os.path.isfile(getSetting("CACHE_PATH")):
            raise RuntimeError("Not logged in!")

    def Match(self, query: str):
        return []

    def Run(self, data: str):
        pass
