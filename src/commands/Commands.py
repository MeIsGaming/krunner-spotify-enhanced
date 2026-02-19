from .AddToQueue import AddToQueue
from .CurrentTrackInfo import CurrentTrackInfo
from .DecreaseVolume import DecreaseVolume
from .EditConfig import EditConfig
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
from .Shuffle import Shuffle
from .FastForward import FastForward
from .Rewind import Rewind
from .Seek import Seek
from .SetVolume import SetVolume
from .Artist import Artist
from .Song import Song
from Config import getCommandName


def executeCommand(command, spotify):
    command_map = {
        getCommandName("NEXT_COMMAND"): Next,
        getCommandName("PREVIOUS_COMMAND"): Previous,
        getCommandName("PAUSE_COMMAND"): Pause,
        getCommandName("RESUME_COMMAND"): Resume,
        getCommandName("DECREASE_VOLUME_COMMAND"): DecreaseVolume,
        getCommandName("INCREASE_VOLUME_COMMAND"): IncreaseVolume,
        getCommandName("PLAY_COMMAND"): Play,
        getCommandName("ADD_TO_QUEUE_COMMAND"): AddToQueue,
        getCommandName("LOGOUT_COMMAND"): Logout,
        getCommandName("LOGIN_COMMAND"): Login,
        getCommandName("CURRENT_TRACK_INFO_COMMAND"): CurrentTrackInfo,
        getCommandName("RELOAD_CONFIG_COMMAND"): ReloadConfig,
        getCommandName("EDIT_CONFIG_COMMAND"): EditConfig,
        getCommandName("SHUFFLE_COMMAND"): Shuffle,
        getCommandName("REPEAT_COMMAND"): Repeat,
        getCommandName("FAST_FORWARD_COMMAND"): FastForward,
        getCommandName("REWIND_COMMAND"): Rewind,
        getCommandName("SEEK_COMMAND"): Seek,
        getCommandName("SET_VOLUME_COMMAND"): SetVolume,
        getCommandName("PLAY_ARTIST_COMMAND"): Artist,
        getCommandName("PLAY_SONG_COMMAND"): Song,
    }
    if command in command_map:
        return command_map[command](spotify)
    raise RuntimeError(f"Unknown command: {command}")