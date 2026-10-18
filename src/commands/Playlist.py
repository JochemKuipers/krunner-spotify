from Config import getCommandName, getSetting
from Util import parse_items, parseSearchQuery

from .Command import Command


class Playlist(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_PLAYLIST_COMMAND"), spotify)

    def Match(self, query: str):
        if query == "":
            return [("", "Enter a playlist name to search", "Spotify", 100, 100, {})]
        query, page = parseSearchQuery(query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        searchResults = self.spotify.search(
            query, int(getSetting("MAX_RESULTS")), offset, "playlist"
        )
        return parse_items(
            searchResults["playlists"]["items"],
            lambda p: p["name"],
            "No playlists found!",
        )

    def Run(self, data: str):
        raise NotImplementedError
