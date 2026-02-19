import re
import webbrowser


def parseSearchQuery(query):
    query = query.lstrip(" ")
    if (query == ""):
        return query, 1
    page = 0
    result = list(filter(None, re.split(r" (p\d+$)", query)))
    if(len(result) == 1):
        return result[0], 1
    else:
        page = int(result[1][1:])
        return result[0], page

def parsePage(query):
    query = query.lstrip(" ")
    page = 1
    if (query == ""):
        return page
    m = re.search('p(\d+)', query)
    return m.group(1)

def parseArtists(results):
    parsedResults = []

    for artist in results['items']:
        parsedResults.append(
            (artist["uri"], artist['name'], "Spotify", 100, 100, {}))
    if(not parsedResults):
        parsedResults.append(
            ("", "No artists found!", "Spotify", 100, 100, {}))
    return parsedResults


def parseTracks(results):
    parsedResults = []
    for track in results["tracks"]["items"]:
        track_details = (track["name"] + " - " +
                         track["album"]["artists"][0]["name"])
        parsedResults.append(
            (track["uri"], track_details, "Spotify", 100, 100, {}))
    if(not parsedResults):
        parsedResults.append(
            ("", "No tracks found!", "Spotify", 100, 100, {}))
    return parsedResults


def parsePlaylists(playlists):
    parsedResults = []
    for playlist in playlists["items"]:
        parsedResults.append(
            (playlist["uri"], playlist["name"], "Spotify", 100, 100, {}))
    if(not parsedResults):
        parsedResults.append(
            ("", "No playlists found!", "Spotify", 100, 100, {}))
    return parsedResults


def parse_spotify_uri(uri: str):
    """
    Parse a Spotify URI into its components.
    
    Args:
        uri: Spotify URI in format 'spotify:type:id'
    """
    parts = uri.split(':')
    if len(parts) != 3 or parts[0] != 'spotify':
        raise ValueError(f"Invalid Spotify URI format: {uri}")
    return parts[0], parts[1], parts[2]


def handle_spotify_uri(spotify, uri: str):
    """
    Handle playback of a Spotify URI. If no active playback session exists, opens the URI in a web browser.
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
        if uri_type in ('track', 'episode'):
            # Tracks and episodes need to be wrapped in a list for uris parameter
            spotify.start_playback(uris=[uri])
        elif uri_type in ('artist', 'playlist', 'album', 'show'):
            # Context URIs (artist, playlist, album, show) use context_uri parameter
            spotify.start_playback(context_uri=uri)
        else:
            raise ValueError(f"Unsupported URI type: {uri_type}")
