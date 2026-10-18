from Config import getCommandName
from Util import parse_duration_seconds

from .Command import Command

_PRESETS = (5, 15, 60, 300, 600)


class RelativeSeek(Command):
    def __init__(self, spotify, sign, config_key, label):
        super().__init__(getCommandName(config_key), spotify)
        self.sign = sign
        self.label = label

    def Match(self, query: str):
        seconds = parse_duration_seconds(query)
        if seconds is not None:
            # rebuild display from original colon form when present
            raw = query.strip(" ")
            parts = raw.split(":")
            if len(parts) == 1:
                desc = f"{self.label}: {parts[0]} sec"
            elif len(parts) == 2:
                desc = f"{self.label}: {parts[0]} min {parts[1]} sec"
            else:
                desc = f"{self.label}: {parts[0]} hr {parts[1]} min {parts[2]} sec"
            return [(self.command + " " + str(seconds), desc, "Spotify", 100, 100, {})]

        options = []
        for i, sec in enumerate(_PRESETS):
            if sec < 60:
                text = f"{self.label} {sec} seconds."
            else:
                text = f"{self.label} {sec // 60} minute" + ("s" if sec != 60 else "")
            options.append(
                (self.command + " " + str(sec), text, "Spotify", 100 - i * 10, 100, {})
            )
        return options

    def Run(self, data: str):
        progress = self.spotify.current_playback()["progress_ms"]
        new_pos = progress + self.sign * int(data) * 1000
        new_pos = max(new_pos, 0)
        self.spotify.seek_track(new_pos)


def FastForward(spotify):
    return RelativeSeek(spotify, 1, "FAST_FORWARD_COMMAND", "FastForward")


def Rewind(spotify):
    return RelativeSeek(spotify, -1, "REWIND_COMMAND", "Rewind")
