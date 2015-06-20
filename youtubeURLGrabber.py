import os
import subprocess
import database
import threading


youTubeMainPageURLs = {}
youTubeMainPageURLs[ ("ArcticEmpire", "Curator") ] = "https://www.youtube.com/user/sheepsempire/videos"  
youTubeMainPageURLs[ ("AirwaveMusic", "Curator") ] = "https://www.youtube.com/user/AirwaveMusicTV/videos"  
youTubeMainPageURLs[ ("TrapCity", "Curator") ] = "https://www.youtube.com/user/OfficialTrapCity/videos"  
youTubeMainPageURLs[ ("ThatNewRave", "Curator") ] = "http://www.youtube.com/user/ThatNewRave/videos"  
youTubeMainPageURLs[ ("MrSuicideSheep", "Curator") ] = "http://www.soundcloud.com/mrsuicidesheep/"
youTubeMainPageURLs[ ("FutureClassic", "Curator") ] = "https://soundcloud.com/futureclassic/"
youTubeMainPageURLs[ ("Complextro", "Curator") ] = "https://soundcloud.com/complextro" 
youTubeMainPageURLs[ ("TheSoundYouNeed", "Curator") ] = "https://www.youtube.com/user/thesoundyouneed1/videos"  
youTubeMainPageURLs[ ("EOENetwork", "Curator") ] = "http://www.youtube.com/user/EOENetwork/videos"  
youTubeMainPageURLs[ ("NewRetroWave", "Curator") ] = "https://soundcloud.com/newretrowave" 
youTubeMainPageURLs[ ("SummerBreeze", "Curator") ] = "https://www.youtube.com/user/Summerbreezemusik/videos"  
youTubeMainPageURLs[ ("FutureSynth", "Curator") ] = "https://soundcloud.com/futuresynth/likes"
youTubeMainPageURLs[ ("BigDataBigData", "Artist") ] = "https://www.youtube.com/user/BigDataBigData/videos"  
youTubeMainPageURLs[ ("Pegboardnerds", "Artist") ] = "http://www.soundcloud.com/pegboardnerds/" 
youTubeMainPageURLs[ ("Madeon", "Artist") ] = "http://www.soundcloud.com/madeon/" 
youTubeMainPageURLs[ ("Kygo", "Artist") ] = "http://www.soundcloud.com/kygo/" 
youTubeMainPageURLs[ ("Jai Wolf", "Artist") ] = "https://soundcloud.com/jaiwolfmusic/tracks"
def doTheThing(page):
	global youTubeMainPageURLs

	print("downloading all URLs for", page)
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
