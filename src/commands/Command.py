"""Abstract base class for Spotify command handlers."""

import os
from abc import ABC, abstractmethod

from Config import getSetting


class Command(ABC):
    """Base command contract used by all command implementations."""

    def __init__(self, command, spotify):
        """Validate auth state and store command context."""
        self.spotify = spotify
        self.command = command
        if not os.path.isfile(getSetting("CACHE_PATH")):
            raise RuntimeError("Not logged in!")

    @abstractmethod
    def Match(self, query: str):
        """Return KRunner matches for the current query."""
        raise NotImplementedError

    @abstractmethod
    def Run(self, data: str):
        """Execute the selected command action."""
        raise NotImplementedError
