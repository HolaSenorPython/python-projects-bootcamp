import requests
import random
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Prompt user for input, and format it. This is the beginning.
print("Welcome! This program will grab music from the Billboard Top 100 from a week in time of YOUR choice, "
      "and then add it to a SPOTIFY playlist for you to enjoy!")
print("(NOTE: You CAN'T look at music from BEFORE YEAR AUGUST 4, 1958.)")
# Inputs from user
year_input = input("Which year would you like to access music from?\n")
month_input = input("Which month? (Write it as a digit. e.g: '05'.)\n")
day_input = input("Which day? (Write it as a digit. Ensure the date exists! Don't look for February 31st! 😅)\n")

# Access the Billboard Top 100 Website with the time period given, and get a list of SONG TITLES and AUTHORS
def get_music_info(date):
    songs = []
    billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept-Language": "en-US,en;q=0.5"
    }
    response = requests.get(url=billboard_url, headers=header)
    response.raise_for_status()
    if response.status_code == 200:
        print(f"Billboard Top 100 successfully accessed for the following date!: {date}")
    billboard_webpage = response.text
    soup = BeautifulSoup(billboard_webpage, "html.parser")
    song_name_tags = soup.select(selector="li.o-chart-results-list__item h3")
    author_name_tags = soup.select("li.o-chart-results-list__item span.a-no-trucate")
    for title_tag, author_tag in zip(song_name_tags, author_name_tags):
        title = title_tag.getText().strip()
        author = author_tag.getText().strip()
        song = (title, author)
        songs.append(song)
    return songs

# Search the songs in the song list on spotify, and then put them into a playlist
def spotify_search(songlist):
    # empty list, will be filled later with a tuple of song + artist, and its unique URI
    songs_with_uris_list = []
    # Authentication stuff
    client_id = os.environ["SPOTIFY_ID"]
    client_secret = os.environ["SPOTIFY_SECRET"]
    redirect_uri = os.environ["SPOTIFY_REDIRECT_URL"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='playlist-modify-public playlist-modify-private user-library-modify'))
    print(f"RAW Redirect URI being used: {repr(redirect_uri)}")
    # Track search
    print("***Every once in a while, i'm gonna print a random song out of the top 100 being searched, so you know i'm "
          "working! 😎***")
    for song_artist_group in songlist:
        track_name = song_artist_group[0]
        artist = song_artist_group[1]
        search_query = f"{track_name} {artist}"
        # Every once in a while, check if its actually searching n stuff.
        if random.randint(1,10) == 10:
            print(f"Searching Spotify for {search_query}....")

        search_result = sp.search(q=search_query, type='track', limit=1)
        song_uri = search_result['tracks']['items'][0]['uri']
        song_with_uri = (search_query, song_uri)
        songs_with_uris_list.append(song_with_uri)
    return songs_with_uris_list

def playlist_maker(song_n_uri_list):
    global time_period
    # Get a list of ONLY track uris:
    uris_only_list = []
    for song_n_uri in song_n_uri_list:
        uri = song_n_uri[1]
        uris_only_list.append(uri)
    # Authentication stuff AGAIN:
    client_id = os.environ["SPOTIFY_ID"]
    client_secret = os.environ["SPOTIFY_SECRET"]
    redirect_uri = os.environ["SPOTIFY_REDIRECT_URL"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='playlist-modify-public playlist-modify-private user-library-modify'))
    # Get my user id
    user_info = sp.current_user()
    user_id = user_info['id']

    # Make playlist
    print(f"Making playlist using the following user id: {user_id}...")
    playlist_info = sp.user_playlist_create(user=user_id,name=f"{time_period} Billboard 100",public=False,
                            description="This playlist contains the top 100 songs from the time period above.")
    playlist_id = playlist_info['id']

    # Add stuff
    print("Adding items to playlist...")
    response = sp.playlist_add_items(playlist_id=playlist_id,items=uris_only_list)
    if 'snapshot_id' in response:
        print("Songs successfully added, and playlist finally made! Go check it out!")
    else:
        print("Oops. Songs weren't added. Something went wrong. 🤔")

# Check if the time period is before August 4, 1958, if not run the shabang bang code
if int(year_input) < 1958:
    print("That date is out of range! Can't you read?? 🫵😔")
elif int(year_input) == 1958 and int(month_input) <= 8 and int(day_input) < 4:
    print("That date is out of range! Can't you read?? 🫵😔")
else:
    time_period = str(year_input + "-" + month_input + "-" + day_input)
    # Print the list of Song name and Artist name tuples
    song_list = get_music_info(time_period)
    print(song_list)
    # Print the list of tuples containing the search query (song + artist) and the track id associated
    songs_and_uri_list = spotify_search(song_list)
    print("These are the songs and their track URIs down below! 👇👇:")
    print(songs_and_uri_list)
    playlist_maker(songs_and_uri_list)