import requests
import json
import sys
import os
from datetime import datetime
from chat_downloader import ChatDownloader

URL = 'https://www.googleapis.com/youtube/v3/'

#ENTER YOUTUBE APIKEY HERE
API_KEY = '';

try:
  def playlist_2_URLs(id: str, next_page_token) -> list:
      params = {
        'key': API_KEY,
        'part': 'snippet',
        'playlistId': id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxRefsults': 100,
      }
      if next_page_token is not None:
        params['pageToken'] = next_page_token
      response = requests.get(URL + 'playlistItems', params=params)
      resource = response.json()

      videos = [];

      try:
        assert "error" not in resource;
      except:
        print(resource["error"]["code"], resource["error"]["errors"][0]["message"]);
        sys.exit(input("An Error Occured."));
      for e in resource['items']:
        fetched_id = e["snippet"]['resourceId']['videoId'];
        videos.append(fetched_id);
        print("Video named {} appended.".format(fetched_id))
      
          
      if "nextPageToken" in resource:
        playlist_2_URLs(id, resource["nextPageToken"]);

      os.system("cls");
      return videos;

  def chatDownloadStarter(videos: list, filename: str) -> None:
    with open(filename + ".txt", mode="w", encoding="utf-8") as f:
      for video_id in videos:
        f.write(video_id + "\n");
        all_messages = chatDownload(video_id = video_id);
        f.write(all_messages);
        f.flush();
      os.system("cls");

  def chatDownload(video_id: str) -> str:
    try:
      chat = ChatDownloader().get_chat(video_id);
      ret = "";
      for message in chat:
        line = "{}\t{}\t{}".format(message["time_text"], message["author"]["name"], message["message"]);
        print(line);
        ret+= "\t" + line + "\n";
      
      return ret;
    except Exception as e:
      print(e);
    return "";

  def main():
    playlistID = input("input playlist URL.");
    print("Thank you.");
    playlistID = playlistID.split("?list=")[-1];
    videos = playlist_2_URLs(id = playlistID, next_page_token = None);
    chatDownloadStarter(videos=videos, filename=playlistID);
    print("Done.")
    input("Press Enter to Exit.");

  if __name__ == "__main__":
    while True:
      main();

except Exception as e:
  print(e);
  input("Press Enter to Exit");
