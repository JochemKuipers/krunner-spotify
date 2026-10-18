from Config import getCommandName, getSetting
from Util import parse_items, parseSearchQuery

from .Command import Command


class MyPlaylist(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_MY_PLAYLIST_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery(query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        playlists = self.spotify.current_user_playlists(
            limit=int(getSetting("MAX_RESULTS")), offset=offset
        )
        return parse_items(
            playlists["items"], lambda p: p["name"], "No playlists found!"
        )

    def Run(self, data: str):
        raise NotImplementedError
