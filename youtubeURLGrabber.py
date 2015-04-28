import os
import subprocess
import database


youTubeMainPageURLs = {"SoundYouNeed": "https://www.youtube.com/user/thesoundyouneed1/videos"}
youTubeMainPageURLs["EOENetwork"] = ""



def addYouTubeCuratorURLs():
	global youTubeMainPageURLs
	for page in youTubeMainPageURLs.keys():
		database.initDB()

		jsonData = str(subprocess.check_output(["youtube-dl", "-J", "--flat-playlist", youTubeMainPageURLs[page]]))
		playlistData = jsonData.split("\"id\": \"")
		playlistData = list(map(lambda x:  "https://www.youtube.com/watch?v=" + x[:x.index('"')], playlistData))[1:]
	
		for videoURL in playlistData:
			database.addURL(videoURL, page)
			print(videoURL)

		database.saveDB()
