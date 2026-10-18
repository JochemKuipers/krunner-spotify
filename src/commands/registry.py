from Config import getCommandName

PLAY_KEYS = (
    "PLAY_ARTIST_COMMAND",
    "PLAY_SONG_COMMAND",
    "PLAY_ARTIST_SONG_COMMAND",
    "PLAY_PLAYLIST_COMMAND",
    "PLAY_MY_PLAYLIST_COMMAND",
    "FOLLOWED_PODCAST_COMMAND",
    "PODCAST_COMMAND",
    "EPISODE_COMMAND",
    "PLAY_TOP_ARTIST_COMMAND",
)

QUEUE_KEYS = (
    "PLAY_SONG_COMMAND",
    "PLAY_ARTIST_SONG_COMMAND",
)

TOP_LEVEL_KEYS = (
    "NEXT_COMMAND",
    "PREVIOUS_COMMAND",
    "PAUSE_COMMAND",
    "RESUME_COMMAND",
    "DECREASE_VOLUME_COMMAND",
    "INCREASE_VOLUME_COMMAND",
    "PLAY_COMMAND",
    "ADD_TO_QUEUE_COMMAND",
    "LOGOUT_COMMAND",
    "LOGIN_COMMAND",
    "CURRENT_TRACK_INFO_COMMAND",
    "RELOAD_CONFIG_COMMAND",
    "EDIT_CONFIG_COMMAND",
    "SHUFFLE_COMMAND",
    "REPEAT_COMMAND",
    "FAST_FORWARD_COMMAND",
    "REWIND_COMMAND",
    "SEEK_COMMAND",
    "SET_VOLUME_COMMAND",
    "PLAY_ARTIST_COMMAND",
    "PLAY_SONG_COMMAND",
)

_REG = None


def _build():
    from .AddToQueue import AddToQueue
    from .Artist import Artist
    from .ArtistSong import ArtistSong
    from .CurrentTrackInfo import CurrentTrackInfo
    from .EditConfig import EditConfig
    from .Episode import Episode
    from .FollowedPodcast import FollowedPodcast
    from .Login import Login
    from .Logout import Logout
    from .MyPlaylist import MyPlaylist
    from .Next import Next
    from .Pause import Pause
    from .Play import Play
    from .Playlist import Playlist
    from .Podcast import Podcast
    from .Previous import Previous
    from .RelativeSeek import FastForward, Rewind
    from .ReloadConfig import ReloadConfig
    from .Repeat import Repeat
    from .Resume import Resume
    from .Seek import Seek
    from .Shuffle import Shuffle
    from .Song import Song
    from .TopArtist import TopArtist
    from .Volume import DecreaseVolume, IncreaseVolume, SetVolume

    return {
        "NEXT_COMMAND": Next,
        "PREVIOUS_COMMAND": Previous,
        "PAUSE_COMMAND": Pause,
        "RESUME_COMMAND": Resume,
        "DECREASE_VOLUME_COMMAND": DecreaseVolume,
        "INCREASE_VOLUME_COMMAND": IncreaseVolume,
        "PLAY_COMMAND": Play,
        "ADD_TO_QUEUE_COMMAND": AddToQueue,
        "LOGOUT_COMMAND": Logout,
        "LOGIN_COMMAND": Login,
        "CURRENT_TRACK_INFO_COMMAND": CurrentTrackInfo,
        "RELOAD_CONFIG_COMMAND": ReloadConfig,
        "EDIT_CONFIG_COMMAND": EditConfig,
        "SHUFFLE_COMMAND": Shuffle,
        "REPEAT_COMMAND": Repeat,
        "FAST_FORWARD_COMMAND": FastForward,
        "REWIND_COMMAND": Rewind,
        "SEEK_COMMAND": Seek,
        "SET_VOLUME_COMMAND": SetVolume,
        "PLAY_ARTIST_COMMAND": Artist,
        "PLAY_SONG_COMMAND": Song,
        "PLAY_ARTIST_SONG_COMMAND": ArtistSong,
        "PLAY_PLAYLIST_COMMAND": Playlist,
        "PLAY_MY_PLAYLIST_COMMAND": MyPlaylist,
        "FOLLOWED_PODCAST_COMMAND": FollowedPodcast,
        "PODCAST_COMMAND": Podcast,
        "EPISODE_COMMAND": Episode,
        "PLAY_TOP_ARTIST_COMMAND": TopArtist,
    }


def registry():
    global _REG
    if _REG is None:
        _REG = _build()
    return _REG


def resolve(command, spotify, keys):
    reg = registry()
    for key in keys:
        if command == getCommandName(key):
            return reg[key](spotify)
    raise RuntimeError("Incorrect command")
