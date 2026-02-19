import os
import subprocess

from Config import CONFIG_FILE_LOCATION, getCommandName, getSetting

from .Command import Command


class EditConfig(Command):
    """Open the local KRunner Spotify config in the configured editor."""

    def __init__(self, spotify):
        self.command = getCommandName("EDIT_CONFIG_COMMAND")

    def Match(self, query: str):
        if os.path.isfile(getSetting("CONFIG_EDITOR")):
            return [
                (self.command, "Edit configuration", "Spotify", 100, 100, {}),
            ]
        else:
            return [
                (
                    self.command,
                    "Given editor: " + getSetting("CONFIG_EDITOR") + " not found!",
                    "Spotify",
                    100,
                    100,
                    {},
                ),
            ]

    def Run(self, data: str):
        """Spawn external editor process for the config file."""
        subprocess.Popen([getSetting("CONFIG_EDITOR"), CONFIG_FILE_LOCATION])
