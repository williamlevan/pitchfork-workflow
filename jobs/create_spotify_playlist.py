from utils.logger import log
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_spotify_playlist(songs, albums):
    """Create a Spotify playlist with the songs and albums"""
    
    # Remove duplicate songs based on artist and song name
    seen_songs = set()
    unique_songs = []
    for song in songs:
        song_key = (song['artist'], song['song'])
        if song_key not in seen_songs:
            seen_songs.add(song_key)
            unique_songs.append(song)
    songs = unique_songs
    
    # Remove duplicate albums based on artist and album name
    seen_albums = set()
    unique_albums = []
    for album in albums:
        album_key = (album['artist'], album['album'])
        if album_key not in seen_albums:
            seen_albums.add(album_key)
            unique_albums.append(album)
    albums = unique_albums
    
    try:
        log(os.getenv("SPOTIFY_CLIENT_ID"))
        log(os.getenv("SPOTIFY_CLIENT_SECRET"))
        log(os.getenv("SPOTIFY_REDIRECT_URI"))
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="playlist-modify-public playlist-modify-private"
        ))
        
        # Get current user
        user = sp.current_user()
        log(f"Authenticated as {user['display_name']}")
        
        # Create playlist
        playlist_name = f"Pitchfork Picks {datetime.now().strftime('%Y-%m-%d')}"
        playlist = sp.user_playlist_create(
            user=user["id"],
            name=playlist_name,
            description="Weekly picks from Pitchfork"
        )
        
        track_uris = []
        
        for song in songs:
            try:
                query = f"artist:{song['artist']} track:{song['song']}"
                results = sp.search(q=query, type="track", limit=1)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    track_uris.append(track['uri'])
                    log(f"Added song: {track['name']} by {track['artists'][0]['name']}")
                else:
                    log(f"Could not find: {song['artist']} - {song['song']}")
                    
            except Exception as e:
                log(f"Error searching for {song['artist']} - {song['song']}: {str(e)}")
        
    except Exception as e:
        log(f"Error creating Spotify playlist: {e}")