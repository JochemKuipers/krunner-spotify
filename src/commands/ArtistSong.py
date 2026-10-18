from Config import getCommandName, getSetting
from Util import parse_items, parseSearchQuery

from .Command import Command


class ArtistSong(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_ARTIST_SONG_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery(query)
        if query != "":
            offset = int(getSetting("MAX_RESULTS")) * (page - 1)
            searchResults = self.spotify.search(
                "artist:" + query, int(getSetting("MAX_RESULTS")), offset, "track"
            )
        else:
            topArtist = self.spotify.current_user_top_artists(limit=1)
            result = self.spotify.artist_top_tracks(topArtist["items"][0]["id"])
            searchResults = {"tracks": {"items": result["tracks"]}}
        return parse_items(
            searchResults["tracks"]["items"],
            lambda t: t["name"] + " - " + t["album"]["artists"][0]["name"],
            "No tracks found!",
        )

    def Run(self, data: str):
        raise NotImplementedError
