from Config import getCommandName, getSetting
from Util import handle_spotify_uri, parse_items, parseSearchQuery

from .Command import Command


class Artist(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_ARTIST_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery(query)
        if query != "":
            offset = int(getSetting("MAX_RESULTS")) * (page - 1)
            searchResults = self.spotify.search(
                "artist:" + query, int(getSetting("MAX_RESULTS")), offset, "artist"
            )["artists"]
        else:
            searchResults = self.spotify.current_user_top_artists(
                limit=int(getSetting("MAX_RESULTS"))
            )
        return parse_items(
            searchResults["items"], lambda a: a["name"], "No artists found!"
        )

    def Run(self, data: str):
        handle_spotify_uri(self.spotify, data)
