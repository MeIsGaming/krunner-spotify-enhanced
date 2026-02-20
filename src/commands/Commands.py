"""Command registry, lookup, and autocomplete helpers."""

from functools import lru_cache
from importlib import import_module

from Config import getCommandName


def _build_command_specs():
    """Return command registry metadata."""
    return [
        ("NEXT_COMMAND", "Next", "Next", "Skip to next track"),
        ("PREVIOUS_COMMAND", "Previous", "Previous", "Go to previous track"),
        ("PAUSE_COMMAND", "Pause", "Pause", "Pause current playback"),
        ("RESUME_COMMAND", "Resume", "Resume", "Resume playback"),
        (
            "DECREASE_VOLUME_COMMAND",
            "DecreaseVolume",
            "DecreaseVolume",
            "Decrease volume",
        ),
        (
            "INCREASE_VOLUME_COMMAND",
            "IncreaseVolume",
            "IncreaseVolume",
            "Increase volume",
        ),
        ("PLAY_COMMAND", "Play", "Play", "Play song, artist or playlist"),
        ("ADD_TO_QUEUE_COMMAND", "AddToQueue", "AddToQueue", "Add song to queue"),
        ("LOGOUT_COMMAND", "Logout", "Logout", "Logout from Spotify"),
        ("LOGIN_COMMAND", "Login", "Login", "Login to Spotify"),
        (
            "CURRENT_TRACK_INFO_COMMAND",
            "CurrentTrackInfo",
            "CurrentTrackInfo",
            "Show current track info",
        ),
        ("RELOAD_CONFIG_COMMAND", "ReloadConfig", "ReloadConfig", "Reload configuration"),
        ("EDIT_CONFIG_COMMAND", "EditConfig", "EditConfig", "Open configuration file"),
        ("SHUFFLE_COMMAND", "Shuffle", "Shuffle", "Toggle shuffle"),
        ("REPEAT_COMMAND", "Repeat", "Repeat", "Set repeat mode"),
        ("FAST_FORWARD_COMMAND", "FastForward", "FastForward", "Seek forward"),
        ("REWIND_COMMAND", "Rewind", "Rewind", "Seek backward"),
        ("SEEK_COMMAND", "Seek", "Seek", "Seek to a position"),
        ("SET_VOLUME_COMMAND", "SetVolume", "SetVolume", "Set absolute volume"),
        ("PLAY_ARTIST_COMMAND", "Artist", "Artist", "Play top tracks by artist"),
        ("PLAY_SONG_COMMAND", "Song", "Song", "Play a song"),
    ]


@lru_cache(maxsize=1)
def _build_command_module_map():
    command_map = {}
    for setting_name, module_name, class_name, _ in _build_command_specs():
        command_map[getCommandName(setting_name)] = (module_name, class_name)
    return command_map


@lru_cache(maxsize=1)
def _build_command_name_map():
    command_map = {}
    for setting_name, _, _, _ in _build_command_specs():
        command_map[getCommandName(setting_name)] = setting_name
    return command_map


@lru_cache(maxsize=1)
def _build_command_descriptions():
    descriptions = {}
    for setting_name, _, _, description in _build_command_specs():
        descriptions[getCommandName(setting_name)] = description
    return descriptions


def _load_command_class(module_name: str, class_name: str):
    module = import_module(f".{module_name}", package=__package__)
    return getattr(module, class_name)


def getCommandNames():
    """Return all command names sorted for autocomplete and lookup."""
    return sorted(_build_command_name_map())


def autocompleteMatches(command_prefix: str):
    """Create autocomplete tuples for a partial command name."""
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
    """Instantiate command handler for a normalized command token."""
    command_name_map = _build_command_name_map()
    if command in command_name_map:
        module_name, class_name = _build_command_module_map()[command]
        command_class = _load_command_class(module_name, class_name)
        return command_class(spotify)
    raise RuntimeError(f"Unknown command: {command}")
