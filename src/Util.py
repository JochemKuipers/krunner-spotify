import re
import webbrowser


def parseSearchQuery(query):
    query = query.lstrip(" ")
    if query == "":
        return query, 1
    bare = re.fullmatch(r"p(\d+)", query)
    if bare:
        return "", int(bare.group(1))
    result = list(filter(None, re.split(r" (p\d+$)", query)))
    if len(result) == 1:
        return result[0], 1
    return result[0], int(result[1][1:])


def parse_duration_seconds(query):
    """Parse 'SS', 'MM:SS', or 'HH:MM:SS' into seconds, or None if invalid."""
    parts = query.strip(" ").split(":")
    if not parts or not all(p.isnumeric() for p in parts):
        return None
    if len(parts) == 1:
        return int(parts[0])
    if len(parts) == 2:
        return 60 * int(parts[0]) + int(parts[1])
    if len(parts) == 3:
        return 3600 * int(parts[0]) + 60 * int(parts[1]) + int(parts[2])
    return None


def parse_items(items, label_fn, empty_msg):
    results = [(item["uri"], label_fn(item), "Spotify", 100, 100, {}) for item in items]
    return results or [("", empty_msg, "Spotify", 100, 100, {})]


def handle_spotify_uri(spotify, uri: str):
    parts = uri.split(":")
    if len(parts) != 3 or parts[0] != "spotify":
        raise ValueError(f"Invalid Spotify URI format: {uri}")
    _, uri_type, uri_id = parts

    devices = spotify.devices()
    if not devices or not devices.get("devices"):
        webbrowser.open(f"https://open.spotify.com/{uri_type}/{uri_id}")
        return

    if uri_type in ("track", "episode"):
        spotify.start_playback(uris=[uri])
    elif uri_type in ("artist", "playlist", "album", "show"):
        spotify.start_playback(context_uri=uri)
    else:
        raise ValueError(f"Unsupported URI type: {uri_type}")


if __name__ == "__main__":
    assert parseSearchQuery("") == ("", 1)
    assert parseSearchQuery("p2") == ("", 2)
    assert parseSearchQuery("foo p3") == ("foo", 3)
    assert parse_duration_seconds("90") == 90
    assert parse_duration_seconds("1:30") == 90
    assert parse_duration_seconds("1:01:40") == 3700
    assert parse_duration_seconds("x") is None
    assert parse_items([], lambda i: i["n"], "empty")[0][1] == "empty"
    print("Util OK")
