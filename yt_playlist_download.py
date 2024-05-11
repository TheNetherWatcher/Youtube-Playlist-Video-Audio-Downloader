import re
import os
from pytube import Playlist
from pytube import YouTube
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

DOWNLOAD_DIR = './'
YOUTUBE_STREAM_AUDIO = '320' 

def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        print(f"The selected directory is: {directory_path}")
    return directory_path

def is_playlist_link(p):
    playlist_patterns = {
        "youtube": r"youtube\.com/playlist\?list=",  # YouTube

    }
    for platform, pattern in playlist_patterns.items():
        if re.search(pattern, p):
            return True  
    if "/playlist/" in p or "/playlists/" in p:
        return True
    
    return False  

# Create the main window
root = tk.Tk()
root.withdraw()

DOWNLOAD_DIR = browse_directory()

root.destroy()

p = input('Enter the playlist URL(make sure it is a public playlist and also you have permission to download files in the selected folder): ')

while not is_playlist_link(p):
    print('Invalid playlist URL. Please enter a valid playlist URL.')
    p = input('Enter the playlist URL: ')

playlist = Playlist(p)

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

print("Total number of videos in the playlist is", len(playlist.video_urls))

for url in playlist.video_urls:
    try:
        yt = YouTube(url)

        video = yt.streams.filter(abr='160kbps').last()

        out_file = video.download(output_path=DOWNLOAD_DIR)
        base, ext = os.path.splitext(out_file)
        new_file = Path(f'{base}.mp3')
        if new_file.exists():
            print(f'{yt.title} already exists at {new_file}, skipping...')
            os.remove(out_file)
        else:
            os.rename(out_file, new_file)
            print(f'{yt.title} has been successfully downloaded to', new_file)
    except Exception as e:
        print(f'ERROR: {yt.title} - {e}')