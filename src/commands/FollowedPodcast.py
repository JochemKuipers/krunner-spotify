from Config import getCommandName, getSetting
from Util import parseSearchQuery

from .Command import Command


class FollowedPodcast(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("FOLLOWED_PODCAST_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery(" a " + query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        savedShows = self.spotify.current_user_saved_shows(
            offset=offset, limit=int(getSetting("MAX_RESULTS"))
        )
        shows = [
            (show["show"]["uri"], show["show"]["name"], "Spotify", 100, 100, {})
            for show in savedShows["items"]
        ]
        return shows or [("", "No podcasts found!", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        raise NotImplementedError
