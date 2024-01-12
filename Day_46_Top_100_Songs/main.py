import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")

all_titles = soup.select("li ul li h3")
all_titles = [title.getText().strip() for title in all_titles]
print(all_titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-private", client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                              redirect_uri="http://example.com"))

user = sp.current_user()["id"]
tracks = []

for name in all_titles:
    try:
        uri = sp.search(q=f"track: {name} year: {year}", limit=1, type="track")["tracks"]["items"][0]["uri"]
        tracks.append(uri)
    except IndexError:
        print("Skipping over the song because it is not in Spotify.")

playlist = sp.user_playlist_create(user, f"{date} Billboard 100", public=False, collaborative=False,
                                   description=f'Billboard top 100 for {date}')
sp.playlist_add_items(playlist["id"], tracks)
