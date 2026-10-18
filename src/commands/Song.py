from Config import getCommandName, getSetting
from Util import handle_spotify_uri, parse_items, parseSearchQuery

from .Command import Command


class Song(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_SONG_COMMAND"), spotify)

    def Match(self, query: str):
        if query != "":
            query, page = parseSearchQuery(query)
            offset = int(getSetting("MAX_RESULTS")) * (page - 1)
            searchResults = self.spotify.search(
                query, int(getSetting("MAX_RESULTS")), offset, "track"
            )
        else:
            searchResults = {
                "tracks": self.spotify.current_user_top_tracks(
                    offset=0, limit=int(getSetting("MAX_RESULTS"))
                )
            }
        return parse_items(
            searchResults["tracks"]["items"],
            lambda t: t["name"] + " - " + t["album"]["artists"][0]["name"],
            "No tracks found!",
        )

    def Run(self, data: str):
        handle_spotify_uri(self.spotify, data)
