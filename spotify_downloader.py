from pytube import Search
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os
from time import sleep
from random import uniform, choice, sample
import math

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
]

def exponential_backoff(attempt, base_delay=5, max_delay=300):
    delay = min(base_delay * (2 ** attempt) + uniform(0, 1), max_delay)
    return delay

def download_with_retry(url, track_name, output_path, max_retries=5):
    for attempt in range(max_retries):
        try:
            audio_download(url, track_name, output_path)
            print(f"Successfully downloaded: {track_name}")
            return
        except Exception as e:
            print(f"Error downloading {track_name}: {str(e)}")
            if attempt < max_retries - 1:
                delay = exponential_backoff(attempt)
                print(f"Retrying in {delay:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
                sleep(delay)
            else:
                print(f"Failed to download {track_name} after {max_retries} attempts.")

def get_playlist_tracks(playlist_id):
    client_credentials_manager = SpotifyClientCredentials(client_id="xxxxxxxxxxxxxxxxxxxx", client_secret="xxxxxxxxxxxxxxxxxxxxx")#insert client id and client secret from created app on https://developer.spotify.com/dashboard 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = sp.playlist_tracks(playlist_id)
    track_names = []
    for item in results['items']:
        track = item['track']
        track_artists = ", ".join([artist["name"] for artist in track['artists']])
        track_names.append(f'{track_artists} - {track['name']}')
    return track_names

def download_from_playlist(track_names, batch_size=5):
    number = 0
    for i in range(0, len(track_names), batch_size):
        batch = track_names[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{math.ceil(len(track_names)/batch_size)}")
        for track in batch:
            url, name = search_youtube(track)
            download_with_retry(url, name, folder_path)
            number += 1
            print(f"Track number {number}. downloaded!")
            sleep_time = uniform(5, 15)
            print(f"Waiting for {sleep_time:.2f} seconds before next download...")
            sleep(sleep_time)
        
        if i + batch_size < len(track_names):
            batch_break = uniform(300, 600)  # 5-10 minutes break between batches
            print(f"Batch complete. Taking a break for {batch_break:.2f} seconds...")
            sleep(batch_break)

def audio_download(url, track_name, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
        }],
        'outtmpl': os.path.join(output_path, track_name),
        'ffmpeg_location': r'C:\Program Files\ffmpeg\bin', #paste location of ffmpeg.exe
        'headers': {'User-Agent': choice(user_agents)},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def search_youtube(query, max_results=2):
    headers = {'User-Agent': choice(user_agents)}
    search = Search(query)
    search._extra_headers = headers
    results = search.results[:max_results]
    list = []
    
    search = Search(query)
    results = search.results[:max_results]

    for idx, video in enumerate(results):
        title = video.title
        video_url = video.watch_url
        list.append([idx+1, title, video_url])

    name = query.split(" - ")
    name[0], name[1] = name[1], name[0]
    name = " - ".join(name)
    print(name)
    return list[0][2], name

def random_tracks(track_names, count, batch_size=5):
    track_names = sample(track_names, count)
    number = 0
    for i in range(0, len(track_names), batch_size):
        batch = track_names[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{math.ceil(len(track_names)/batch_size)}")
        for track in batch:
            url, name = search_youtube(track)
            download_with_retry(url, name, folder_path)
            number += 1
            print(f"Track number {number} downloaded!")
            sleep_time = uniform(5, 15)
            print(f"Waiting for {sleep_time:.2f} seconds before next download...")
            sleep(sleep_time)
        
        if i + batch_size < len(track_names):
            batch_break = uniform(300, 600)  # 5-10 minutes break between batches
            print(f"Batch complete. Taking a break for {batch_break:.2f} seconds...")
            sleep(batch_break)

def tracks_in_range(first, last, track_names, batch_size=5):
    number = 0
    for i in range(first-1, last, batch_size):
        batch = track_names[i:min(i+batch_size, last)]
        print(f"Processing batch {i//batch_size + 1}/{math.ceil(len(track_names)/batch_size)}")
        for track in batch:
            url, name = search_youtube(track)
            download_with_retry(url, name, folder_path)
            number += 1
            print(f"Track number {number}. downloaded!")
            sleep_time = uniform(5, 15)
            print(f"Waiting for {sleep_time:.2f} seconds before next download...")
            sleep(sleep_time)
        
        if i + batch_size < last:
            batch_break = uniform(300, 600)  # 5-10 minutes break between batches
            print(f"Batch complete. Taking a break for {batch_break:.2f} seconds...")
            sleep(batch_break)
    
if __name__ == "__main__":
    playlist_id = "yyyyyyyyyyyyyyyyy" #id of your playlist
    folder_path = r"C:\Path\to\your\destination\folder" # change your destination path
    
    track_names = get_playlist_tracks(playlist_id)
    print(f"Total tracks: {len(track_names)}")

    #tracks_in_range(52, len(track_names), track_names) #download from 52. to last one
    download_from_playlist(track_names) #download all from playlist
    #number_of_tracks = 50
    #random_tracks(track_names, number_of_tracks) #download random 50 tracks from playlist
