import webbrowser

from Config import getCommandName, getSetting

from .Artist import Artist
from .ArtistSong import ArtistSong
from .Command import Command
from .Episode import Episode
from .FeaturedPlaylist import FeaturedPlaylist
from .FollowedPodcast import FollowedPodcast
from .MyPlaylist import MyPlaylist
from .Playlist import Playlist
from .Podcast import Podcast
from .Song import Song
from .TopArtist import TopArtist


class Play(Command):
    """Dispatcher command for playback-oriented subcommands and URI playback."""

    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_COMMAND"), spotify)

    def _command_map(self):
        """Return subcommand -> handler class mapping for play command namespace."""
        return {
            getCommandName("PLAY_ARTIST_COMMAND"): Artist,
            getCommandName("PLAY_SONG_COMMAND"): Song,
            getCommandName("PLAY_SONG_BY_ARTIST_COMMAND"): ArtistSong,
            getCommandName("PLAY_FEATURED_PLAYLIST_COMMAND"): FeaturedPlaylist,
            getCommandName("PLAY_PLAYLIST_COMMAND"): Playlist,
            getCommandName("PLAY_MY_PLAYLIST_COMMAND"): MyPlaylist,
            getCommandName("FOLLOWED_PODCAST_COMMAND"): FollowedPodcast,
            getCommandName("PODCAST_COMMAND"): Podcast,
            getCommandName("EPISODE_COMMAND"): Episode,
            getCommandName("PLAY_TOP_ARTIST_COMMAND"): TopArtist,
        }

    def Match(self, query: str):
        """Return prefixed suggestions from selected play subcommand."""
        arguments = ""
        if " " in query:
            command, arguments = query.split(" ", 1)
        else:
            command = query

        try:
            results = self.executeCommand(command).Match(arguments)
            prefixed_results = []
            for uri, title, icon, relevance, score, actions in results:
                prefixed_results.append(
                    (f"{self.command} {uri}", title, icon, relevance, score, actions)
                )
            return prefixed_results
        except RuntimeError:
            return [("", "Invalid command", "Spotify", 100, 100, {})]

    def Run(self, data: str):
        """Run playback using current device, or open URI in browser if no device exists."""
        if data == "":
            return

        if not self.spotify.current_playback():
            parts = data.split(":")
            if len(parts) >= 3:
                webbrowser.open("https://open.spotify.com/track/" + parts[2])
            return

        elif "track" in data or "episode" in data:
            self.spotify.start_playback(uris=[data])
        elif "show" in data or "artist" in data or "playlist" in data:
            self.spotify.start_playback(context_uri=data)

    def executeCommand(self, command: str):
        """Instantiate handler for a play subcommand token."""
        if getSetting("CASE_SENSITIVE") == "False":
            command = command.upper()
        command_map = self._command_map()
        if command in command_map:
            return command_map[command](self.spotify)
        raise RuntimeError("Incorrect command")
