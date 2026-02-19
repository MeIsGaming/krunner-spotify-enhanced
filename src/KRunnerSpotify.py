import logging
import os
import sys

import dbus.service
import spotipy
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib  # type: ignore
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyPKCE

from commands import Commands
from Config import getBoolSetting, getCommandName, getSetting
from Util import handle_spotify_uri

# Add the src directory to Python path so imports work when run via D-Bus
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)


DBusGMainLoop(set_as_default=True)

LOG_LEVEL = os.getenv("KRUNNER_SPOTIFY_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.WARNING))
logger = logging.getLogger("KRunnerSpotify")

objpath = "/KRunnerSpotify"
iface1 = "org.kde.krunner1"
iface2 = "org.kde.krunner2"


class Runner(dbus.service.Object):
    """DBus-backed KRunner runner for Spotify commands."""

    def __init__(self):
        """Initialize DBus object and Spotify PKCE client."""
        dbus.service.Object.__init__(
            self, dbus.service.BusName("org.kde.KRunnerSpotify", dbus.SessionBus()), objpath
        )
        os.makedirs(os.path.dirname(getSetting("CACHE_PATH")), exist_ok=True)
        self.auth_manager = SpotifyPKCE(
            client_id=getSetting("CLIENT_ID"),
            cache_path=getSetting("CACHE_PATH"),
            redirect_uri=getSetting("REDIRECT_URI"),
            scope=getSetting("ACCES_SCOPE"),
        )
        self.spotify = spotipy.Spotify(auth_manager=self.auth_manager)

    def _get_prefix(self) -> str:
        """Return normalized command prefix from config, with safe fallback."""
        prefix = getSetting("COMMAND_PREFIX").strip().lower()
        return prefix or "spe"

    def _get_accepted_prefixes(self) -> list[str]:
        """Return accepted prefixes, optionally including legacy alias."""
        prefixes = [self._get_prefix()]
        if getBoolSetting("ENABLE_LEGACY_SP_ALIAS", False) and "sp" not in prefixes:
            prefixes.append("sp")
        return prefixes

    def _normalize_command(self, command: str) -> str:
        """Normalize command according to CASE_SENSITIVE setting."""
        if getSetting("CASE_SENSITIVE") == "False":
            return command.upper()
        return command

    def _autocomplete_with_prefix(self, prefix: str, command_prefix: str):
        """Return autocomplete results with runner prefix in the command payload."""
        matches = Commands.autocompleteMatches(command_prefix)
        prefixed_matches = []
        for command, title, icon, relevance, score, actions in matches:
            prefixed_matches.append(
                (f"{prefix} {command}", title, icon, relevance, score, actions)
            )
        return prefixed_matches

    def _spotify_error_message(self, error: SpotifyException) -> str:
        """Create user-facing message for common Spotify API failures."""
        if error.http_status == 403:
            return (
                "Spotify API denied request (403). Add your account in Spotify "
                "Dashboard > Users and Access, then run: spe login"
            )
        if error.http_status == 401:
            return "Spotify token expired/invalid. Run: spe login"
        return f"Spotify API error ({error.http_status})"

    def _match_impl(self, query: str):
        """Handle KRunner Match requests and return result tuples."""
        lowered_query = query.lower().strip()
        accepted_prefixes = self._get_accepted_prefixes()
        if lowered_query in accepted_prefixes:
            return self._autocomplete_with_prefix(lowered_query, "")

        matched_prefix = ""
        for prefix in accepted_prefixes:
            expected_prefix = prefix + " "
            if query.lower().startswith(expected_prefix):
                matched_prefix = expected_prefix
                break

        if matched_prefix == "":
            return []

        query = query[len(matched_prefix) :].strip()

        if query == "":
            return self._autocomplete_with_prefix(matched_prefix.strip(), "")

        arguments = ""
        if " " in query:
            command, arguments = query.split(" ", 1)
        else:
            command = query
        try:
            command = self._normalize_command(command)

            if arguments == "" and command not in Commands.getCommandNames():
                return self._autocomplete_with_prefix(matched_prefix.strip(), command)

            return Commands.executeCommand(command, self.spotify).Match(arguments)
        except RuntimeError as e:
            if str(e) == "Not logged in!":
                return [
                    (
                        getCommandName("LOGIN_COMMAND"),
                        "Not logged in, click to login",
                        "Spotify",
                        100,
                        100,
                        {},
                    )
                ]
            logger.warning("Match runtime error: %s", e)
            return []
        except SpotifyException as e:
            return [("", self._spotify_error_message(e), "Spotify", 100, 100, {})]
        except Exception as e:
            logger.exception("Unexpected match error: %s", e)
            return []

    def _run_impl(self, data: str, action_id: str):
        """Handle KRunner Run requests for selected command/result."""
        del action_id

        # If data is a Spotify URI (from search results), handle it directly
        if data.startswith("spotify:"):
            handle_spotify_uri(self.spotify, data)
            return

        for prefix in self._get_accepted_prefixes():
            expected_prefix = prefix + " "
            if data.lower().startswith(expected_prefix):
                data = data[len(expected_prefix) :].strip()
                break

        if data == "":
            return

        command = data
        if " " in data:
            command, data = data.split(" ", 1)
        else:
            data = ""

        command = self._normalize_command(command)
        try:
            Commands.executeCommand(command, self.spotify).Run(data)
        except RuntimeError as e:
            logger.warning("Run runtime error: %s", e)
        except SpotifyException as e:
            logger.warning("Spotify API error during run (%s): %s", e.http_status, e)
        except Exception as e:
            logger.exception("Unexpected run error: %s", e)

    # Support both krunner1 (Plasma 6) and krunner2 (Plasma 5) interfaces
    @dbus.service.method(iface1, in_signature="s", out_signature="a(sssida{sv})")
    @dbus.service.method(iface2, in_signature="s", out_signature="a(sssida{sv})")
    def Match(self, query: str):
        return self._match_impl(query)

    @dbus.service.method(iface1, in_signature="ss")
    @dbus.service.method(iface2, in_signature="ss")
    def Run(self, data: str, action_id: str):
        self._run_impl(data, action_id)


runner = Runner()
loop = GLib.MainLoop()
loop.run()
