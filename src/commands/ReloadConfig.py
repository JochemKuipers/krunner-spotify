from Config import getCommandName, loadConfig

from .Command import Command


class ReloadConfig(Command):
    def __init__(self, spotify):
        self.command = getCommandName("RELOAD_CONFIG_COMMAND")

    def Match(self, query: str):
        return [
            (self.command, "Reload configuration", "Spotify", 100, 100, {}),
        ]

    def Run(self, data: str):
        loadConfig()
