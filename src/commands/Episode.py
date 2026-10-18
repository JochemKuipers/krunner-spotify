from Config import getCommandName, getSetting
from Util import parseSearchQuery

from .Command import Command


class Episode(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("EPISODE_COMMAND"), spotify)

    def Match(self, query: str):
        _, page = parseSearchQuery(query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        playbackDetails = self.spotify.currently_playing(additional_types="episode")
        if playbackDetails["item"]["type"] != "episode":
            return [("", "No podcast is being played!", "Spotify", 100, 100, {})]

        episodes = self.spotify.show_episodes(
            playbackDetails["item"]["show"]["id"],
            offset=offset,
            limit=int(getSetting("MAX_RESULTS")),
        )
        results = []
        relevance = 100
        for episode in episodes["items"]:
            results.append(
                (
                    episode["uri"],
                    episode["name"],
                    self._icon(episode, playbackDetails),
                    relevance,
                    100,
                    {},
                )
            )
            relevance -= 1
        return results

    def Run(self, data: str):
        raise NotImplementedError

    def _icon(self, episode, playbackDetails):
        icon = "NewSpotify"
        if episode["resume_point"]["resume_position_ms"] != 0:
            icon = "ResumeSpotify"
        if episode["resume_point"]["fully_played"]:
            icon = "FullyPlayedSpotify"
        if episode["id"] == playbackDetails["item"]["id"]:
            icon = "CurrentlyPlayingSpotify"
        return icon
