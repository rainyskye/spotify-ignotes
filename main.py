import spotipy
from instagrapi import Client
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

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

# Cut it off WOOOOOOOOO
def truncate(s):
    if len(s) > 20:
        return s[:17] + "..."
    else:
        return s

# Ensure it works the first time
track_name = None

while True:
    # Get currently playing track
    current_track = sp.current_playback()

    # Get current track info and set it as the user's note if track_name changes
    if current_track is not None and 'item' in current_track:
        new_track_name = current_track['item']['name']

        if new_track_name != track_name:
            artist_name = current_track['item']['artists'][0]['name']
            truncated_track_name = truncate(new_track_name)
            truncated_artist_name = truncate(artist_name)
            content = (f"🎵 Playing: {truncated_track_name} by {truncated_artist_name}")
            check_string_length(content)
            note = cl.create_note(content, 0)
            print(f"Track Changed! Set note to '{content}'")

            # Update track_name to the new_track_name
            track_name = new_track_name
        else:
            print("Track not changed, sleeping for 10 seconds.")
    else:
        print("No track is currently playing.")

    # Add a delay to avoid continuous API requests
    time.sleep(10)  # Adjust the delay time as needed