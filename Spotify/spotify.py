import pandas as pd 
import spotipy 
 
""" Necesitamos los modulos de spotipy y pandas. Si nos los tenemos, los instalaremos escribiendo en la consola:
    pip install spotipy
    pip install pandas
"""

sp = spotipy.Spotify() 
from spotipy.oauth2 import SpotifyClientCredentials 
cid ="18fe3109b7e24c838602101d29ff7c1c"
secret = "46c0157100944f1ab23aed67a0dcd617"


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 
sp.trace=False 

playlist = sp.user_playlist("spotifycharts", "37i9dQZEVXbNFJfN1Vw8d9", fields="tracks,next") 
tracks = playlist["tracks"] 
songs = tracks["items"]

ids = []
song = []
artist = []

for i in range(len(songs)): 
	s = songs[i]["track"]
	ids.append(s["id"]) 
	song.append([s["id"],s["name"],s["popularity"],s["album"]["id"],s["album"]["name"],s["album"]["images"][0]["url"],s["album"]["release_date"],s["artists"][0]["id"],s["artists"][0]["name"]])

	a = sp.artist(s["artists"][0]["id"])
	img =""
	if len(a["images"]) >0:
		img = a["images"][0]["url"]

	artist.append([a["id"],a["name"],a["popularity"],a["followers"]["total"],img])

dataArtists = pd.DataFrame(artist)

features = sp.audio_features(ids) 
df = pd.DataFrame(features)

dataSongs = pd.DataFrame(song)

while tracks["next"]:	
	
	tracks = sp.next(tracks)
	songs = tracks["items"]
	
	ids = []
	song2 = []
	artist2 = []
	
	for i in range(len(songs)):
		s = songs[i]["track"]
		ids.append(s["id"])
		song2.append([s["id"],s["name"],s["popularity"],s["album"]["id"],s["album"]["name"],s["album"]["images"][0]["url"],s["album"]["release_date"],s["artists"][0]["id"],s["artists"][0]["name"]])

		a = sp.artist(s["artists"][0]["id"])
		img = ""
		if len(a["images"]) >0:
			img = a["images"][0]["url"]
		artist2.append([a["id"],a["name"],a["popularity"],a["followers"]["total"],img])

	features2 = sp.audio_features(ids) 
	df2= pd.DataFrame(features2)
	df = pd.concat([df,df2])
	
	dataSongs2 = pd.DataFrame(song2)
	dataSongs = pd.concat([dataSongs,dataSongs2])
	
	dataArtists2 = pd.DataFrame(artist2)
	dataArtists = pd.concat([dataArtists,dataArtists2])

df.to_csv("onedayonesong-features", sep='\t', encoding='utf-8')

dataSongs.columns=["id","name","popularity","id_album","album_name","url_album_photo","album_release_date","artist_id","artist_name"]
dataSongs.to_csv("onedayonesong-datasong", sep='\t', encoding='utf-8')

dataArtists.columns=["id", "name", "popularity", "followers", "total"]
dataArtists.to_csv("onedayonesong-dataartist", sep='\t', encoding='utf-8')