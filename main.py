import spotipy
from instagrapi import Client
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load from .env
load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Setup Instagram authentication
cl = Client()
cl.login(username, password)

# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="user-read-playback-state"))



# Make sure it's not over 60 characters
# Instagram may see a failed request for 60+ chars and get sus :3
def check_string_length(input_string):
    if len(input_string) > 60:
        raise ValueError("IT'S TOO FUCKING BIG YOU BUMBLING FORK")
    else:
        print("eheheh, it's okay!! continuing :3")

# Get currently playing track
current_track = sp.current_playback()

# Get current track info and set it as the users note
if current_track is not None and 'item' in current_track:
    track_name = current_track['item']['name']
    artist_name = current_track['item']['artists'][0]['name']
    content = (f"🎵 Playing: {track_name} by {artist_name}")
    check_string_length(content)
    note = cl.create_note(content, 0)
    print(f"Set note to '{content}'")
else:
    print("No track is currently playing.")

