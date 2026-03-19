import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv()

def init_spotify():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def search_tracks(sp, query):
    results = sp.search(q=query, type='track', limit=10)
    return results['tracks']['items']

def extract_track_info(track):
    if track is None:
        return None
    
    track_info = {
        'track_id': track.get('id'),
        'track_name': track.get('name'),
        'artist_name': track['artists'][0]['name'] if track.get('artists') else None,
        'artist_id': track['artists'][0]['id'] if track.get('artists') else None,
        'album_name': track['album']['name'] if track.get('album') else None,
        'release_date': track['album']['release_date'] if track.get('album') else None,
        'popularity': track.get('popularity', 0),
        'duration_ms': track.get('duration_ms', 0)
    }
    return track_info

def collect_music_data(queries, output_file):
    print("Initializing Spotify client...")
    sp = init_spotify()
    
    all_tracks = []
    
    for query in queries:
        print(f"Searching for: {query}")
        tracks = search_tracks(sp, query)
        all_tracks.extend(tracks)
        time.sleep(0.5)
    
    print(f"Found {len(all_tracks)} tracks total")
    
    print("Extracting track information...")
    tracks_data = []
    for track in all_tracks:
        track_info = extract_track_info(track)
        if track_info and track_info['track_id']:
            tracks_data.append(track_info)
    
    df = pd.DataFrame(tracks_data)
    df = df.drop_duplicates(subset='track_id')
    
    df['duration_min'] = df['duration_ms'] / 60000
    df['release_year'] = pd.to_datetime(df['release_date']).dt.year
    
    df.to_csv(output_file, index=False)
    print(f"\nData saved to {output_file}")
    print(f"Collected {len(df)} unique tracks with {len(df.columns)} features")
    
    return df

if __name__ == "__main__":
    search_queries = [
        "pop 2024",
        "hip hop 2024",
        "rock 2024",
        "edm 2024",
        "r&b 2024",
        "indie 2024",
        "country 2024",
        "latin 2024",
        "kpop 2024",
        "jazz 2024"
    ]
    
    output_file = "data/raw/spotify_music_data.csv"
    
    df = collect_music_data(search_queries, output_file)
    print("\nFirst few rows:")
    print(df.head())
    print("\nTop 10 most popular:")
    print(df.nlargest(10, 'popularity')[['track_name', 'artist_name', 'popularity']])