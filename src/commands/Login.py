import os

from spotipy.exceptions import SpotifyException

from Config import getCommandName, getSetting

from .Command import Command


class Login(Command):
    """Login command with stale-cache recovery and permission diagnostics."""

    def __init__(self, spotify):
        try:
            super().__init__(getCommandName("LOGIN_COMMAND"), spotify)
        except RuntimeError:
            pass

    def Match(self, query: str):
        cache_path = getSetting("CACHE_PATH")
        if not os.path.isfile(cache_path):
            return [(getCommandName("LOGIN_COMMAND"), "Log into Spotify", "Spotify", 100, 100, {})]

        try:
            self.spotify.current_user()
            return [("", "Already logged in", "Spotify", 100, 100, {})]
        except SpotifyException as error:
            if error.http_status == 403:
                return [
                    (
                        getCommandName("LOGIN_COMMAND"),
                        "Access denied (403): add account in Spotify Dashboard > Users and Access",
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            return [
                (
                    getCommandName("LOGIN_COMMAND"),
                    "Session invalid, click to re-login",
                    "Spotify",
                    100,
                    100,
                    {},
                )
            ]

    def Run(self, data: str):
        cache_path = getSetting("CACHE_PATH")
        if os.path.isfile(cache_path):
            os.remove(cache_path)

        self.spotify.current_user()
