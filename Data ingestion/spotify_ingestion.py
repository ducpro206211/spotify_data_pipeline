import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from datetime import datetime
import json
from kafka import KafkaProducer
import time

# Spotify credentials
CLIENT_ID = '3ac00c95599a46228eaa42963f543fce'
CLIENT_SECRET = '3cd6e255c9b442bfa56e0e568751c10f'
SPOTIFY_CLIENT_ID='3ac00c95599a46228eaa42963f543fce'
SPOTIFY_CLIENT_SECRET='3cd6e255c9b442bfa56e0e568751c10f'
# Redpanda connection
REDPANDA_BROKERS = 'localhost:9092'
TOPIC_PREFIX = 'spotify_data'

# List of artists with their IDs and names
ARTISTS = {
    '0ixzjrK1wkN2zWBXt3VW3W': 'yuuri',
    '1n7bHz03w0ew7UNCw1dAiA': 'halosy',
    '4DDoAL8n6ob19r3jOZEbJI': 'kananishino',
    '29PeG6G6C986jnRPBECm4D': 'Mihimaru GT',
    '1snhtMLeb2DYoMOcVbb8iB': 'Kenshi Yoneru',
    '4KxdU52S7CLwdVtDDgh0Gf': 'Rapwipds',
    '0B1ce3uNrzkdm76NXI4mhX': 'Tani yuuki',
    '4QvgGvpgzgyUOo8Yp8LDm9': 'MRs green Apple',
    '7JthQ6zwNzfxRfIEjp6wUs': 'Hiraidai',
    '1Y5vJqABeI6QI6R95EDV6o': 'Tuki',
    '5cW1SVDUXXzsj3eFT7Gmta': 'AiScream',
    '1zPnpAM7fGFr7pl8OSNvak': 'Kisida Kyodan & The Akebosi Rockets',
    '56DDzGJXY0xndL9wu9aHUD': 'Yugo Kanno',
    '3PWp9R5HvbQgxI5KBx5kVd': 'Kanna-Boon',
    '5ohV9BStGDoxJ9HlAlHXCd': 'Unlimited Tone',
    '64tJ2EAv1R6UaZqc4iOCyj': 'YOASOBI',
    '5iZSZ19Lnt6iQTDITRF7Mn': 'fear and loathing in las vegas',
    '0blbVefuxOGltDBa00dspv': 'Lisa',
    '0pWR7TsFhvSCnbmHDjWgrE': 'Creept Nut'
}

class RedPandas:
    def __init__(self, brokers):
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send(self, topic, data):
        self.producer.send(topic, data)
        self.producer.flush()

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    ))

def process_artist(artist_id, artist_name, sp, rp):
    try:
        artist_urn = f'spotify:artist:{artist_id}'
        artist_data = sp.artist(artist_urn)
        artist_data['timestamp'] = datetime.now().isoformat()
        
        rp.send(
            topic=f"{TOPIC_PREFIX}_artists",
            data=artist_data
        )
        print(f"✅ Successfully processed {artist_name}")
        return True
    except Exception as e:
        print(f"❌ Error processing {artist_name}: {str(e)}")
        return False

def main():
    # Initialize Redpanda producer
    rp = RedPandas(brokers=REDPANDA_BROKERS)
    
    # Initialize Spotify client
    sp = get_spotify_client()
    
    success_count = 0
    error_count = 0
    
    print("\n🔄 Starting artist data ingestion...")
    
    for artist_id, artist_name in ARTISTS.items():
        if process_artist(artist_id, artist_name, sp, rp):
            success_count += 1
        else:
            error_count += 1
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)
    
    print("\n📊 Ingestion Summary:")
    print(f"✅ Successfully processed: {success_count} artists")
    print(f"❌ Failed to process: {error_count} artists")
    print(f"🌐 Check Redpanda UI (if enabled) at: http://localhost:9644")

if __name__ == "__main__":
    main()
