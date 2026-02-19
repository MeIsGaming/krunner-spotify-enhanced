from functools import lru_cache

from Config import getCommandName

from .AddToQueue import AddToQueue
from .Artist import Artist
from .CurrentTrackInfo import CurrentTrackInfo
from .DecreaseVolume import DecreaseVolume
from .EditConfig import EditConfig
from .FastForward import FastForward
from .IncreaseVolume import IncreaseVolume
from .Login import Login
from .Logout import Logout
from .Next import Next
from .Pause import Pause
from .Play import Play
from .Previous import Previous
from .ReloadConfig import ReloadConfig
from .Repeat import Repeat
from .Resume import Resume
from .Rewind import Rewind
from .Seek import Seek
from .SetVolume import SetVolume
from .Shuffle import Shuffle
from .Song import Song


def _build_command_specs():
    return [
        ("NEXT_COMMAND", Next, "Skip to next track"),
        ("PREVIOUS_COMMAND", Previous, "Go to previous track"),
        ("PAUSE_COMMAND", Pause, "Pause current playback"),
        ("RESUME_COMMAND", Resume, "Resume playback"),
        ("DECREASE_VOLUME_COMMAND", DecreaseVolume, "Decrease volume"),
        ("INCREASE_VOLUME_COMMAND", IncreaseVolume, "Increase volume"),
        ("PLAY_COMMAND", Play, "Play song, artist or playlist"),
        ("ADD_TO_QUEUE_COMMAND", AddToQueue, "Add song to queue"),
        ("LOGOUT_COMMAND", Logout, "Logout from Spotify"),
        ("LOGIN_COMMAND", Login, "Login to Spotify"),
        ("CURRENT_TRACK_INFO_COMMAND", CurrentTrackInfo, "Show current track info"),
        ("RELOAD_CONFIG_COMMAND", ReloadConfig, "Reload configuration"),
        ("EDIT_CONFIG_COMMAND", EditConfig, "Open configuration file"),
        ("SHUFFLE_COMMAND", Shuffle, "Toggle shuffle"),
        ("REPEAT_COMMAND", Repeat, "Set repeat mode"),
        ("FAST_FORWARD_COMMAND", FastForward, "Seek forward"),
        ("REWIND_COMMAND", Rewind, "Seek backward"),
        ("SEEK_COMMAND", Seek, "Seek to a position"),
        ("SET_VOLUME_COMMAND", SetVolume, "Set absolute volume"),
        ("PLAY_ARTIST_COMMAND", Artist, "Play top tracks by artist"),
        ("PLAY_SONG_COMMAND", Song, "Play a song"),
    ]


@lru_cache(maxsize=1)
def _build_command_map():
    command_map = {}
    for setting_name, command_class, _ in _build_command_specs():
        command_map[getCommandName(setting_name)] = command_class
    return command_map


@lru_cache(maxsize=1)
def _build_command_descriptions():
    descriptions = {}
    for setting_name, _, description in _build_command_specs():
        descriptions[getCommandName(setting_name)] = description
    return descriptions


def getCommandNames():
    return sorted(_build_command_map())


def autocompleteMatches(command_prefix: str):
    command_prefix = command_prefix or ""
    descriptions = _build_command_descriptions()
    matches = []
    for command_name in getCommandNames():
        if command_prefix and not command_name.startswith(command_prefix):
            continue
        matches.append(
            (
                command_name,
                descriptions.get(command_name, "Spotify command"),
                "Spotify",
                100,
                100,
                {},
            )
        )
    return matches


def executeCommand(command, spotify):
    command_map = _build_command_map()
    if command in command_map:
        return command_map[command](spotify)
    raise RuntimeError(f"Unknown command: {command}")
