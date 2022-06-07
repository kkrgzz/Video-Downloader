from re import X
import requests
import json
import os

class redditDownloader:
    def __init__(self, pageURL):
        self.pageURL = pageURL
        self.jsonURL = None
        self.jsonResponse = None
        self.mediaURL = None
        self.audioURL = None

        self.videoTempName = "video.mp4"
        self.audioTempName = "audio.mp3"
        self.outputName = "output.mp4"


        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        self.__prepLink()
        self.__downloadMedia()
    
    def __prepLink(self):
        if self.pageURL[len(self.pageURL) - 1] == '/':
            self.jsonURL = self.pageURL[:len(self.pageURL) - 1] + ".json"
            print(self.jsonURL)
        else:
            self.jsonURL = self.pageURL + ".json"

        self.jsonResponse = requests.get(self.jsonURL, headers=self.headers)

        if self.jsonResponse.status_code != 200:
            print("Error! Check URL Again!")
        else:
            self.mediaURL = self.jsonResponse.json()[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]
            self.audioURL = "https://v.redd.it/" + self.mediaURL.split("/")[3]+"/DASH_audio.mp4"
            
    def __downloadMedia(self):
        with open(self.videoTempName, "wb") as f:
            g = requests.get(self.mediaURL, stream=True)
            f.write(g.content)

        with open(self.audioTempName, "wb") as f:
            g = requests.get(self.audioURL, stream=True)
            f.write(g.content)
        
        media_path = str(os.getcwd() + '\\bin\\ffmpeg -i ' + self.videoTempName + ' -i ' + self.audioTempName + ' -c copy ' + self.outputName)
        print(media_path)
        #os.system(media_path)


        

    