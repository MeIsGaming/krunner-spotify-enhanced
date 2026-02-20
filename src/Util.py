"""Utility helpers for query parsing and Spotify URI playback handling."""

import re
import webbrowser


def parseSearchQuery(query):
    """Split a search query and optional page suffix (`pN`)."""
    query = query.lstrip(" ")
    if query == "":
        return query, 1
    page = 0
    result = list(filter(None, re.split(r" (p\d+$)", query)))
    if len(result) == 1:
        return result[0], 1
    else:
        page = int(result[1][1:])
        return result[0], page


def parsePage(query):
    """Parse page number suffix from query, defaulting to page 1."""
    query = query.lstrip(" ")
    page = 1
    if query == "":
        return page
    m = re.search(r"p(\d+)", query)
    if m is None:
        return page
    return int(m.group(1))


def parseArtists(results):
    """Map Spotify artist results to KRunner tuple format."""
    parsed_results = []

    for artist in results["items"]:
        parsed_results.append((artist["uri"], artist["name"], "Spotify", 100, 100, {}))
    if not parsed_results:
        parsed_results.append(("", "No artists found!", "Spotify", 100, 100, {}))
    return parsed_results


def parseTracks(results):
    """Map Spotify track results to KRunner tuple format."""
    parsed_results = []
    for track in results["tracks"]["items"]:
        track_details = track["name"] + " - " + track["album"]["artists"][0]["name"]
        parsed_results.append((track["uri"], track_details, "Spotify", 100, 100, {}))
    if not parsed_results:
        parsed_results.append(("", "No tracks found!", "Spotify", 100, 100, {}))
    return parsed_results


def parsePlaylists(playlists):
    """Map Spotify playlist results to KRunner tuple format."""
    parsed_results = []
    for playlist in playlists["items"]:
        parsed_results.append((playlist["uri"], playlist["name"], "Spotify", 100, 100, {}))
    if not parsed_results:
        parsed_results.append(("", "No playlists found!", "Spotify", 100, 100, {}))
    return parsed_results


def parse_spotify_uri(uri: str):
    """
    Parse a Spotify URI into its components.

    Args:
        uri: Spotify URI in format 'spotify:type:id'
    """
    parts = uri.split(":")
    if len(parts) != 3 or parts[0] != "spotify":
        raise ValueError(f"Invalid Spotify URI format: {uri}")
    return parts[0], parts[1], parts[2]


def handle_spotify_uri(spotify, uri: str):
    """
    Handle playback of a Spotify URI.

    If no active playback session exists, opens the URI in a web browser.
    Otherwise, starts playback using the Spotify API.

    Args:
        spotify: Spotipy client instance
        uri: Spotify URI to play
    """
    _, uri_type, uri_id = parse_spotify_uri(uri)

    if not spotify.current_playback():
        # No active playback - open in browser
        webbrowser.open(f"https://open.spotify.com/{uri_type}/{uri_id}")
    else:
        # Active playback - use API
        if uri_type in ("track", "episode"):
            # Tracks and episodes need to be wrapped in a list for uris parameter
            spotify.start_playback(uris=[uri])
        elif uri_type in ("artist", "playlist", "album", "show"):
            # Context URIs (artist, playlist, album, show) use context_uri parameter
            spotify.start_playback(context_uri=uri)
        else:
            raise ValueError(f"Unsupported URI type: {uri_type}")
