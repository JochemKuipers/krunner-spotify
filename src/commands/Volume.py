from Config import getCommandName, getSetting

from .Command import Command

DEVICES_WITHOUT_VOLUME_CONTROL = ("Tablet", "Smartphone")

_MODE_KEYS = {
    "inc": "INCREASE_VOLUME_COMMAND",
    "dec": "DECREASE_VOLUME_COMMAND",
    "set": "SET_VOLUME_COMMAND",
}

# Shared across Match calls in one KRunner session
_state = {
    "inc": {"count": 0, "vol": 0},
    "dec": {"count": 0, "vol": 0},
    "set": {"inc": 0, "dec": 0, "vol": 0},
}


class Volume(Command):
    def __init__(self, spotify, mode):
        super().__init__(getCommandName(_MODE_KEYS[mode]), spotify)
        self.mode = mode

    def Match(self, query: str):
        playback = self.spotify.current_playback()
        if playback["device"]["type"] in DEVICES_WITHOUT_VOLUME_CONTROL:
            return [
                (
                    "",
                    "Volume cannot be controlled on the current device",
                    "Spotify",
                    100,
                    100,
                    {},
                )
            ]

        query = query.strip(" ")
        if self.mode == "set":
            return self._match_set(query, playback)
        return self._match_step(query, playback)

    def Run(self, data: str):
        st = _state[self.mode]
        if self.mode == "set":
            self.spotify.volume(int(data))
            return
        delta = int(data) if self.mode == "inc" else -int(data)
        st["vol"] = max(0, min(100, st["vol"] + delta))
        self.spotify.volume(st["vol"])

    def _match_step(self, query, playback):
        st = _state[self.mode]
        sign = 1 if self.mode == "inc" else -1
        char = getSetting(
            "INCREASE_VOLUME_CHARACTER"
            if self.mode == "inc"
            else "DECREASE_VOLUME_CHARACTER"
        )
        verb = "Increase" if self.mode == "inc" else "Decrease"
        limit = 100 if self.mode == "inc" else 0
        at_limit_msg = f"Volume is already {limit}%"

        if st["count"] == 0:
            st["vol"] = playback["device"]["volume_percent"]

        if query.isnumeric() and len(query) > 0:
            volume = int(query)
            if volume < 0 or volume > 100:
                return [
                    (
                        " ",
                        "Volume has to be between 1 and 100%",
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            if st["vol"] == limit:
                return [("", at_limit_msg, "Spotify", 100, 100, {})]
            return [
                (
                    self.command + " " + str(volume),
                    f"{verb} volume with {volume}%",
                    "Spotify",
                    100,
                    100,
                    {},
                )
            ]

        if len(query) > 0 and query[0] == char and query == len(query) * query[0]:
            diff = len(query) - st["count"]
            st["count"] = len(query)
            if abs(diff) in (0, 1):
                if diff == 0:
                    diff = 1
                st["vol"] = st["vol"] + int(getSetting("VOLUME_STEP")) * diff * sign
                st["vol"] = max(0, min(100, st["vol"]))
                self.spotify.volume(st["vol"])
                if st["vol"] == limit and diff * sign > 0:
                    return [("", at_limit_msg, "Spotify", 100, 100, {})]
                return [
                    (
                        "",
                        "Volume is now set to: " + str(st["vol"]),
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            return []

        if (self.mode == "inc" and st["vol"] >= 100) or (
            self.mode == "dec" and st["vol"] <= 0
        ):
            return [("", at_limit_msg, "Spotify", 100, 100, {})]
        return [
            (self.command + " 10", f"{verb} volume with 10%", "Spotify", 100, 100, {}),
            (self.command + " 25", f"{verb} volume with 25%", "Spotify", 100, 80, {}),
            (self.command + " 50", f"{verb} volume with 50%", "Spotify", 100, 60, {}),
            (self.command + " 100", f"{verb} volume with 100%", "Spotify", 100, 40, {}),
        ]

    def _match_set(self, query, playback):
        st = _state["set"]
        inc_c = getSetting("INCREASE_VOLUME_CHARACTER")
        dec_c = getSetting("DECREASE_VOLUME_CHARACTER")

        if query.isnumeric() and len(query) > 0:
            volume = int(query)
            if volume < 0 or volume > 100:
                return [
                    (
                        " ",
                        "Volume has to be between 1 and 100%",
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            return [
                (
                    self.command + " " + str(volume),
                    "Set volume to " + str(volume) + "%",
                    "Spotify",
                    100,
                    100,
                    {},
                )
            ]

        if query and all(c in (inc_c + dec_c) for c in query):
            decrease = query.count(dec_c)
            increase = query.count(inc_c)
            if (decrease == 0 and increase == 1) or (decrease == 1 and increase == 0):
                st["vol"] = playback["device"]["volume_percent"]
            if decrease > st["dec"]:
                st["vol"] -= int(getSetting("VOLUME_STEP")) * abs(decrease - st["dec"])
            elif increase > st["inc"]:
                st["vol"] += int(getSetting("VOLUME_STEP")) * abs(increase - st["inc"])
            elif decrease < st["dec"]:
                st["vol"] += int(getSetting("VOLUME_STEP")) * abs(decrease - st["dec"])
            elif increase < st["inc"]:
                st["vol"] -= int(getSetting("VOLUME_STEP")) * abs(increase - st["inc"])
            st["dec"], st["inc"] = decrease, increase
            st["vol"] = max(0, min(100, st["vol"]))
            self.spotify.volume(st["vol"])
            if st["vol"] == 0:
                return [(" ", "Min volume reached!", "Spotify", 100, 100, {})]
            if st["vol"] == 100:
                return [(" ", "Max volume reached!", "Spotify", 100, 100, {})]
            return [
                (
                    " ",
                    "Volume has been set to: " + str(st["vol"]) + "%",
                    "Spotify",
                    100,
                    100,
                    {},
                )
            ]

        return [
            (self.command + " 10", "Set volume to 10%", "Spotify", 100, 100, {}),
            (self.command + " 25", "Set volume to 25%", "Spotify", 100, 80, {}),
            (self.command + " 50", "Set volume to 50%", "Spotify", 100, 60, {}),
            (self.command + " 100", "Set volume to 100%", "Spotify", 100, 40, {}),
        ]


def IncreaseVolume(spotify):
    return Volume(spotify, "inc")


def DecreaseVolume(spotify):
    return Volume(spotify, "dec")


def SetVolume(spotify):
    return Volume(spotify, "set")
