import requests
import json

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

API_key = os.getenv("API_key")
channel_handle = "MrBeast"
def get_playlist_id():
    try: 
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_key}"
        response = requests.get(url)
        #HTTP status code of 200-299 means success codes
        response.raise_for_status()

        #parse the response using JSON
        data = response.json()
        #print(json.dumps(data, indent=4))

        channel_items = data['items'][0]
        channel_playlistId = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        raise e


max_results = 50

def get_video_id(playlistId):
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={API_key}"
    page_token = None
    video_ids = []

    try:
        while True:
            url = base_url
            if page_token:
                url = url + f"&pageToken={page_token}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []): #here, because it can happen that 'items' would be empty, to avoid KeyError, we set the default of empty list
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            page_token = data.get("nextPageToken")
            if not page_token:
                break

        return video_ids



    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlistId = get_playlist_id()
    get_video_id(playlistId)


