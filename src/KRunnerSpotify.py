import os
import sys
import logging

# Add the src directory to Python path so imports work when run via D-Bus
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from commands import Commands
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from spotipy.oauth2 import SpotifyPKCE
from Config import getCommandName, getSetting
from Util import handle_spotify_uri
import dbus.service
import spotipy

DBusGMainLoop(set_as_default=True)

LOG_LEVEL = os.getenv("KRUNNER_SPOTIFY_LOG_LEVEL", "WARNING").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.WARNING))
logger = logging.getLogger("KRunnerSpotify")

objpath = "/KRunnerSpotify"
iface1 = "org.kde.krunner1"
iface2 = "org.kde.krunner2"


class Runner(dbus.service.Object):
    def __init__(self):
        dbus.service.Object.__init__(self, dbus.service.BusName(
            "org.kde.KRunnerSpotify", dbus.SessionBus()), objpath)
        os.makedirs(os.path.dirname(getSetting("CACHE_PATH")), exist_ok=True)
        self.auth_manager = SpotifyPKCE(client_id=getSetting("CLIENT_ID"),
                                        cache_path=getSetting("CACHE_PATH"),
                                        redirect_uri=getSetting(
                                            "REDIRECT_URI"),
                                        scope=getSetting("ACCES_SCOPE"))
        self.spotify = spotipy.Spotify(auth_manager=self.auth_manager)

    def _match_impl(self, query: str):
        prefix = getSetting("COMMAND_PREFIX").strip().lower()
        if prefix == "":
            prefix = "spe"

        expected_prefix = prefix + " "
        if not query.lower().startswith(expected_prefix):
            return []
        
        query = query[len(expected_prefix):]
        
        arguments = ""
        if(" " in query):
            command, arguments = query.split(" ", 1)
        else:
            command = query
        try:
            if(getSetting("CASE_SENSITIVE") == "False"):
                command = command.upper()
            return Commands.executeCommand(command, self.spotify).Match(arguments)
        except RuntimeError as e:
            if(str(e) == "Not logged in!"):
                return [(getCommandName("LOGIN_COMMAND"), "Not logged in, click to login", "Spotify", 100, 100, {})]
            logger.warning("Match runtime error: %s", e)
            return []
        except Exception as e:
            logger.exception("Unexpected match error: %s", e)
            return []

    def _run_impl(self, data: str, action_id: str):
        # If data is a Spotify URI (from search results), handle it directly
        if data.startswith("spotify:"):
            handle_spotify_uri(self.spotify, data)
            return
        
        prefix = getSetting("COMMAND_PREFIX").strip().lower()
        if prefix == "":
            prefix = "spe"

        expected_prefix = prefix + " "
        if data.lower().startswith(expected_prefix):
            data = data[len(expected_prefix):]
        
        command = data
        if(" " in data):
            command, data = data.split(" ", 1)
        else:
            data = ""
        try:
            Commands.executeCommand(command, self.spotify).Run(data)
        except RuntimeError as e:
            logger.warning("Run runtime error: %s", e)
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
