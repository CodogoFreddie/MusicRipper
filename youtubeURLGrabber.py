import os
import subprocess
import database
import threading


youTubeMainPageURLs = {}
youTubeMainPageURLs["ArcticEmpire"] = "https://www.youtube.com/user/sheepsempire/videos"  
youTubeMainPageURLs["ThatNewRave"] = "http://www.youtube.com/user/ThatNewRave/videos"  
youTubeMainPageURLs["MrSuicideSheep"] = "http://www.soundcloud.com/mrsuicidesheep/"
youTubeMainPageURLs["FutureClassic"] = "https://soundcloud.com/futureclassic/"
youTubeMainPageURLs["Madeon"] = "http://www.soundcloud.com/madeon/" 
youTubeMainPageURLs["Complextro"] = "https://soundcloud.com/complextro" 
youTubeMainPageURLs["Kygo"] = "http://www.soundcloud.com/kygo/" 
youTubeMainPageURLs["TheSoundYouNeed"] = "https://www.youtube.com/user/thesoundyouneed1/videos"  
youTubeMainPageURLs["EOENetwork"] = "http://www.youtube.com/user/EOENetwork/videos"  
youTubeMainPageURLs["NewRetroWave"] = "https://soundcloud.com/newretrowave" 
youTubeMainPageURLs["SummerBreeze"] = "https://www.youtube.com/user/Summerbreezemusik/videos"  
youTubeMainPageURLs["BigDataBigData"] = "https://www.youtube.com/user/BigDataBigData/videos"  
youTubeMainPageURLs["Pegboardnerds"] = "http://www.soundcloud.com/pegboardnerds/" 
youTubeMainPageURLs["FutureSynth"] = "https://soundcloud.com/futuresynth/likes"
def doTheThing(page):
	global youTubeMainPageURLs

	print("starting thread for", page)
	jsonData = str(subprocess.check_output(["youtube-dl", "-J", "--flat-playlist", youTubeMainPageURLs[page]]))
	print("got data for", page)

	if "youtube" in youTubeMainPageURLs[page]:
		playlistData = jsonData.split("\"id\": \"")
		playlistData = list(map(lambda x:  "https://www.youtube.com/watch?v=" + x[:x.index('"')], playlistData))[1:]
	else:
		playlistData = jsonData.split("\"webpage_url\": \"")
		playlistData = list(map(lambda x: x[:x.index('"')], playlistData))[1:]

	for videoURL in playlistData:
		database.addURL(videoURL, page)
		print('\t', videoURL)


def addYouTubeCuratorURLs():
	global youTubeMainPageURLs
	threads = {}
	for page in youTubeMainPageURLs.keys():
		database.initDB()
		doTheThing(page)
		database.saveDB()