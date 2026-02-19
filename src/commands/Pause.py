from Config import getCommandName

from .Command import Command


class Pause(Command):
    def __init__(self, spotify):
        super().__init__(getCommandName("PAUSE_COMMAND"), spotify)

    def Match(self, query: str):
        return [(self.command, "Pause current song", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        playback = self.spotify.current_playback()
        if playback and playback.get("device") and playback["device"].get("id"):
            self.spotify.pause_playback(device_id=playback["device"]["id"])
            return
        self.spotify.pause_playback()
