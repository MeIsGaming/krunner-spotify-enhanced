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
    def __init__(self, spotify):
        super().__init__(getCommandName("PLAY_COMMAND"), spotify)

    def Match(self, query: str):
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
        if getSetting("CASE_SENSITIVE") == "False":
            command = command.upper()
        if command == getCommandName("PLAY_ARTIST_COMMAND"):
            return Artist(self.spotify)
        elif command == getCommandName("PLAY_SONG_COMMAND"):
            return Song(self.spotify)
        elif command == getCommandName("PLAY_SONG_BY_ARTIST_COMMAND"):
            return ArtistSong(self.spotify)
        elif command == getCommandName("PLAY_FEATURED_PLAYLIST_COMMAND"):
            return FeaturedPlaylist(self.spotify)
        elif command == getCommandName("PLAY_PLAYLIST_COMMAND"):
            return Playlist(self.spotify)
        elif command == getCommandName("PLAY_MY_PLAYLIST_COMMAND"):
            return MyPlaylist(self.spotify)
        elif command == getCommandName("FOLLOWED_PODCAST_COMMAND"):
            return FollowedPodcast(self.spotify)
        elif command == getCommandName("PODCAST_COMMAND"):
            return Podcast(self.spotify)
        elif command == getCommandName("EPISODE_COMMAND"):
            return Episode(self.spotify)
        elif command == getCommandName("PLAY_TOP_ARTIST_COMMAND"):
            return TopArtist(self.spotify)
        raise RuntimeError("Incorrect command")
