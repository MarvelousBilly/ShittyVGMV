from googleapiclient.discovery import build
from tqdm import tqdm
import json
import os
import random
import psutil
import requests, subprocess
import time

youtube = build('youtube', 'v3', developerKey='AIzaSyDs0eDvDoKoJwoWoBZ4L2XJFU2e4xbVG7E')

def fetch_playlist_items(playlist_name, page_token=None):
    return youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_name,
        maxResults=50,  # Maximum number of results per page
        pageToken=page_token
    ).execute()

def grabItems(playlist_name):
    songs = []
    next_page_token = None
    playlist_items = fetch_playlist_items(playlist_name)
    total_pages = playlist_items['pageInfo']['totalResults'] // 50
    
    for pos in tqdm (range(total_pages), desc="Adding list " + playlist_name):
        playlist_items = fetch_playlist_items(playlist_name, page_token=next_page_token)
        
        # Process each video
        for item in playlist_items['items']:
            if(item['snippet']['title'] != 'Private video'):
                newSong = {"title": item['snippet']['title'], "url": 'https://www.youtube.com/watch?v=' + item['snippet']['resourceId']['videoId'], "image":item['snippet']['thumbnails']['high']['url']}
                songs.append(newSong)

        next_page_token = playlist_items.get('nextPageToken')
        if not next_page_token:
            break
    return songs
            

def main():
    file_path = 'videos.json' 
    ALLSONGS = []

    while True:
        playlist = input("Input playlist ID, \"Stop\", or \"Chase\" (Ex: PL1gPdX7Zdh797jb4PuTw9fA58Kuz0Dh9S): ")
        if(playlist == "Chase" or playlist == "chase"):
            ALLSONGS.extend(grabItems("PL1gPdX7Zdh797jb4PuTw9fA58Kuz0Dh9S"))
            ALLSONGS.extend(grabItems("PL1gPdX7Zdh7_Fw5ncdX892hMZBsK3LlLN"))
            break
        elif(playlist == "Stop" or playlist == "stop"):
            break
        else:
            grabItems(playlist)
        
    with open(file_path, 'w') as file:
        json.dump(ALLSONGS, file)
        
        

if __name__ == "__main__":
    main()