import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

gitload_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = "The Teskey Brothers"

result = sp.search(q=artist_name, type='artist', limit=1)

artist = result['artists']['items'][0]

print(f"Nombre del artista: {artist['name']}")
print(f"URL de Spotify: {artist['external_urls']['spotify']}")
print(f"Imagen del artista: {artist['images'][0]['url'] if artist['images'] else 'No imagen disponible'}")

artist_id = artist['id']

top_tracks = sp.artist_top_tracks(artist_id)['tracks']

tracks_data = {
    'Nombre Canción': [track['name'] for track in top_tracks],
    'Popularidad': [track['popularity'] for track in top_tracks],
    'URL': [track['external_urls']['spotify'] for track in top_tracks],
    'Duración (segundos)': [track['duration_ms'] / 1000 for track in top_tracks]  # Convertir ms a segundos
}

df = pd.DataFrame(tracks_data)

df_sorted = df.sort_values(by='Popularidad', ascending=True)

print(df_sorted.head(3))

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Duración (segundos)', y='Popularidad', marker='o')

plt.title('Relación entre Duración de la Canción y Popularidad')
plt.xlabel('Duración de la Canción (segundos)')
plt.ylabel('Popularidad')
plt.grid(True)

plt.show()
