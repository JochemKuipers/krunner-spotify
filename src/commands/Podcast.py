from Config import getCommandName, getSetting
from Util import parse_items, parseSearchQuery

from .Command import Command


class Podcast(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PODCAST_COMMAND"), spotify)

    def Match(self, query: str):
        query, page = parseSearchQuery(query)
        offset = int(getSetting("MAX_RESULTS")) * (page - 1)
        results = self.spotify.search(
            q=query, limit=int(getSetting("MAX_RESULTS")), offset=offset, type="show"
        )
        return parse_items(
            results["shows"]["items"],
            lambda s: s["name"] + " - " + s["publisher"],
            "No podcasts found!",
        )

    def Run(self, data: str):
        raise NotImplementedError
