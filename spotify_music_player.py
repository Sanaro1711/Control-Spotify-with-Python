import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Authenticate with Spotify API
scope = "user-read-playback-state user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

class MusicPlayerSpotify:
    """a class to get music and its informtion from Spotify"""

    def __init__(self):
        """initialise attributes of the class"""
        #self.song_name = song_name

    def running_program(self):
        """Keep calling the options"""
        active = True
        while active == True:
            active = self.get_user_input()


    def user_options(self):
        """Prints out the options the user has in this music player"""
        print("\nOPTIONS")
        print("1. Play a single song")
        print("2. Add a song to queue")
        print("3. Get information about a current")
        print("4. Add a list of songs to queue")
        print("5. Get list of top songs")
        print("6. Get list of top artists")
        print("7. Wait before next input")
        print("8. Quit")


    def get_user_input(self):
        """Get the song/list of songs user wants to play - and add to queue"""
        self.user_options()
        try:
            user_input = int(input("Choose an option: "))
        except Exception as e:
            print(f"Exception {e} occurred")
            return True #to keep the program running again


        if (user_input == 1):
            user_song = input("Enter a song to play: ")
            user_artist = input("Enter artist name: ")
            try:
                self.play_song(f"{user_song} artist:{user_artist}")
            except Exception:
                print("Sorry song not found!")

        elif (user_input == 2):
            user_song = input("Enter a song to add to queue: ")
            user_artist = input("Enter artist name: ")
            try:
                self.add_to_queue(f"{user_song} artist:{user_artist}")
            except Exception:
                print("Sorry song not found!")

        elif (user_input == 3):
            self.check_current_song_data()


        elif (user_input == 4):
            number_of_songs = int(input("How many songs would you like to add: "))
            for i in range(number_of_songs):
                user_song = input("Enter song name: ")
                user_artist = input("Enter artist name: ")
                self.add_to_queue(f"{user_song} artist:{user_artist}")

        elif (user_input == 5):
            print("YOUR TOP SONGS ARE:")
            self.get_top_tracks()

        elif (user_input == 6):
            print("YOUR TOP ARTISTS ARE:")
            self.get_top_artists()

        elif (user_input == 7):
            print("Waiting...")
            time.sleep(30)

        elif (user_input == 8):
            return False


        time.sleep(5) #have a bit of delay between next input
        return True



    def search_song(self, song_name):
        """Search for the song user asks for"""
        query = f"track:{song_name}"
        self.result = sp.search(q=query, limit=1, type='track')


    def check_current_song_data(self):
        """Print the name and artist of the current song playing"""
        current_track_data = sp.current_user_playing_track() #all data of current song

        #song nane
        if current_track_data:
            current_track_name = current_track_data['item']['name']
            #song artist
            current_track_artist = current_track_data['item']['artists'][0]['name']
            print(f"Current Song: {current_track_name} - {current_track_artist}")

        else:
            print("No song playing right now")

    def add_to_queue(self, song_name):
        """Add a given song to queue"""
        self.search_song(song_name)
        self.get_meta_data(self.result)
        try:
            sp.add_to_queue(self.track_uri)
            print("SONG HAS BEEN ADDED TO QUEUE")

        except Exception:
            print("Sorry song not found")

    def play_song(self, song_name):
        """plays the song user enters"""
        self.search_song(song_name)
        self.get_meta_data(self.result)
        print(f"Now Playing {self.song_name} by {self.artist_name}")
        sp.start_playback(None, uris=[self.track_uri])

    def get_meta_data(self, track_data):
        """Return the metadata of whatever song user wants"""

        #sp now has all spotify methods i can access
        if track_data['tracks']['items']: #making sure it exists
            self.track = track_data['tracks']['items'][0] #holds all the information about track
            self.song_name = self.track['name']
            self.album_name = self.track['album']['name']
            self.artist_name = self.track['artists'][0]['name']
            self.release_date = self.track['album']['release_date']
            self.popularity = self.track['popularity']
            self.track_uri = self.track['uri']
            self.ablbum_cover_art = self.track['album']['images'][0]['url']

            # Print metadata
            print()
            print(f"\n🎵 Song: {self.song_name}")
            print(f"🎤 Artist: {self.artist_name}")
            print(f"💿 Album: {self.album_name}")
            print(f"📅 Release Date: {self.release_date}")
            print(f"⭐ Popularity: {self.popularity}")
            print(f"🎼 Track URI: {self.track_uri}")

        else:
            print("Song not found.")

    def get_top_tracks(self):
        """Prints out the usert top songs based on conditions"""
        #first printing out top songs:

        num = int(input("How many top songs do you want to see: "))
        t_range = input("What time range do you want to see results for: "
                            "(short_term, medium_term or long_term): ")

        try:
            top_tracks = sp.current_user_top_tracks(limit=num, time_range=t_range)

            if not top_tracks['items']:
                print("No top tracks found. Try a different time range.")

            else:
                print("\n🎵 Your Top Tracks:")
                for i, track in enumerate(top_tracks['items'], 1):
                    print(f"{i}. {track['name']} - {track['artists'][0]['name']}")

        except spotipy.exceptions.SpotifyException as e:
            print(f"Error fetching top tracks: {e}")

    def get_top_artists(self):
        """Prints out the user's top artists based on conditions"""

        num = int(input("How many top artists you want to see: "))
        t_range = input("What time range do you want to see results for: "
                            "(short_term, medium_term or long_term): ")

        try:
            top_artists = sp.current_user_top_artists(limit = num, time_range = t_range)

            if not top_artists['items']:
                print("No top artists found. Try a different time range.")

            else:
                for i, artist in enumerate(top_artists['items'], 1):
                    print(f"{i}. {artist['name']}")

        except Exception:
            print("failed to find any...try for a different time_range")








instance = MusicPlayerSpotify().running_program()
