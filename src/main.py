import requests
import spotipy
import video
import json
import spotipy.util as util

#youtube HTML request parameters
BASE_URL = "https://www.googleapis.com/youtube/v3/playlistItems?"
PARAMS = "part=snippet&playlistId="
API_KEY = "&key=AIzaSyCsAOCC3nTA34ZXpXjdvsfHCjZHJ-lhplc"

def get_youtube_playlist(playlist_url):

    # this returns a list of Video objects that have all the necessary
    # details to add them into the spotify playlist
    playlist_id = parse_playlist_id(playlist_url)
    videos = generate_video_list(request_playlist_videos(playlist_id))
    return videos


def parse_playlist_id(playlist_url):
    index1 = playlist_url.find("list=")
    index2 = playlist_url.find("&", index1)
    if index2 is -1:
        return playlist_url[index1+5:]
    else:
        return playlist_url[index1+5:index2]


def request_playlist_videos(playlist_id):
    r = requests.get(BASE_URL + PARAMS + playlist_id + API_KEY).json()
    items = r['items']
    # it's possible that only one page is used, therefore need a try block outside the loop
    try:
        next_page = r['nextPageToken']
    except KeyError:
        return items

    while True:
        r = requests.get(BASE_URL + PARAMS + playlist_id + API_KEY + "&pageToken=" + next_page).json()
        items += r['items']
        try:
            next_page = r['nextPageToken']
        except KeyError:
            break
    return items


def generate_video_list(items):

    # returns list of video objects

    video_list = []
    
    for item in items:
        title = item['snippet']['title']
        v = video.Video(title)
        video_list.append(v)
    return video_list


def spotify_authentication_token(username):

    #spotify token request parameters
    SPOTIPY_CLIENT_ID = 'f19773a1ef114cc3944aefd8e3dec235'
    SPOTIPY_CLIENT_SECRET = '0bb41eb569334b55b40f3fdbaee4d444'
    SPOTIPY_REDIRECT_URI = 'http://localhost/'
    SCOPE = 'playlist-modify-public'

    return util.prompt_for_user_token(username, SCOPE, SPOTIPY_CLIENT_ID,
                                      SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)


if __name__ == '__main__':
    username = input("Enter your username: ")
    s = spotipy.Spotify(auth=spotify_authentication_token(username))

    playlist = get_youtube_playlist(input("Enter the URL for the playlist to convert: "))
    print("Fetched playlist!")

    song_uris = []

    for vid in playlist:
        #print("Searching for", vid.video_title)
        results = s.search(q=vid.get_search_query(), type='track', limit=5)
        songs_in_results = min(results['tracks']['total'],5)
        if songs_in_results is not 0:
            for song in range(songs_in_results):
                artist = results['tracks']['items'][song]['artists'][0]['name']
                isSong = bool(vid.artist == video.Video.simplifyTitle(artist))
                if isSong:
                    song_uris.append(results['tracks']['items'][song]['uri'])
                    print("ADDED: ", vid.video_title)
                    break
                if song is 5:
                    print("COULD NOT FIND: ", vid.video_title)
    
    print("")
    
    yts_playlist = s.user_playlist_create(username, "YouTube To Spotify", True)

    for track in song_uris:
        s.user_playlist_add_tracks(username, yts_playlist['id'], [track])

    print("Added", len(song_uris), "out of", len(playlist), "songs.")

