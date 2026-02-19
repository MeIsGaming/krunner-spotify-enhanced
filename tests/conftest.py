from pathlib import Path


TEST_CONFIG = """[Settings]
VOLUME_STEP = 10
MAX_RESULTS = 5
SPOTIFY_URL = https://open.spotify.com
ACCES_SCOPE = user-modify-playback-state user-read-playback-state
CLIENT_ID = test-client-id
REDIRECT_URI = http://127.0.0.1:3000/callback
CACHE_PATH = ~/.cache/KRunnerSpotify/.cache
CASE_SENSITIVE = False
COMMAND_PREFIX = spe
ENABLE_LEGACY_SP_ALIAS = False
CONFIG_EDITOR = /usr/bin/true
INCREASE_VOLUME_CHARACTER = +
DECREASE_VOLUME_CHARACTER = -

[CommandNames]
ADD_TO_QUEUE_COMMAND = Add
CURRENT_TRACK_INFO_COMMAND = TrackInfo
DECREASE_VOLUME_COMMAND = DecVol
EDIT_CONFIG_COMMAND = EditConfig
EPISODE_COMMAND = Episode
FAST_FORWARD_COMMAND = FastForward
FOLLOWED_PODCAST_COMMAND = FollowedPodcast
INCREASE_VOLUME_COMMAND = IncVol
LOGIN_COMMAND = Login
LOGOUT_COMMAND = Logout
NEXT_COMMAND = Next
PAUSE_COMMAND = Pause
PLAY_ARTIST_COMMAND = artist
PLAY_COMMAND = Play
PLAY_FEATURED_PLAYLIST_COMMAND = featured
PLAY_MY_PLAYLIST_COMMAND = myplaylist
PLAY_PLAYLIST_COMMAND = playlist
PLAY_SONG_BY_ARTIST_COMMAND = byArtist
PLAY_SONG_COMMAND = song
PLAY_TOP_ARTIST_COMMAND = topArtist
PODCAST_COMMAND = Podcast
PREVIOUS_COMMAND = Previous
RELOAD_CONFIG_COMMAND = ReloadConfig
REPEAT_COMMAND = Repeat
RESUME_COMMAND = Resume
REWIND_COMMAND = Rewind
SEEK_COMMAND = Seek
SET_VOLUME_COMMAND = SetVol
SHUFFLE_COMMAND = Shuffle
"""


def ensure_test_config() -> Path:
    config_dir = Path.home() / ".config" / "KRunner-Spotify"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "KRunner-Spotify.config"
    config_file.write_text(TEST_CONFIG, encoding="utf-8")

    cache_dir = Path.home() / ".cache" / "KRunnerSpotify"
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / ".cache").touch()
    return config_file
