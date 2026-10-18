from Config import getCommandName, getSetting
from Util import parse_items, parseSearchQuery

from .Command import Command


class TopArtist(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_TOP_ARTIST_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery("a " + query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        searchResults = self.spotify.current_user_top_artists(
            limit=int(getSetting("MAX_RESULTS")), offset=offset
        )
        return parse_items(
            searchResults["items"], lambda a: a["name"], "No artists found!"
        )

    def Run(self, data: str):
        raise NotImplementedError
