import os
import subprocess
import database
import threading


youTubeMainPageURLs = {}
youTubeMainPageURLs[ ("TrapCity", "Curator") ] = "https://www.youtube.com/user/OfficialTrapCity/videos"
youTubeMainPageURLs[ ("MrSuicideSheep", "Curator") ] = "https://www.youtube.com/user/MrSuicideSheep"
youTubeMainPageURLs[ ("TheSoundYouNeed", "Curator") ] = "https://www.youtube.com/user/thesoundyouneed1/videos"
youTubeMainPageURLs[ ("EOENetwork", "Curator") ] = "http://www.youtube.com/user/EOENetwork/videos"
youTubeMainPageURLs[ ("BigDataBigData", "Artist") ] = "https://www.youtube.com/user/BigDataBigData/videos"
youTubeMainPageURLs[ ("Madeon", "Artist") ] = "https://www.youtube.com/user/MadeonVEVO/video"
youTubeMainPageURLs[ ("Kygo", "Artist") ] = "https://www.youtube.com/user/KygoOfficialVEVO/video"
youTubeMainPageURLs[ ("Pentatonix", "Artist") ] = "https://www.youtube.com/user/PTXofficial/videos"
youTubeMainPageURLs[ ("Disciples", "Artist") ] = "https://www.youtube.com/user/DisciplesLDN/videos"
youTubeMainPageURLs[ ("ElectronicGems", "Curator") ] = "https://www.youtube.com/user/HungOverGargoyle/videos"
youTubeMainPageURLs[ ("VulfPeck", "Artist") ] = "https://www.youtube.com/user/DJparadiddle/videos"
youTubeMainPageURLs[ ("MajesticCasual", "Curator") ] = "https://www.youtube.com/user/majesticcasual/videos"
def doTheThing(page):
	global youTubeMainPageURLs

	print("downloading all URLs for", page)
	jsonData = str(subprocess.check_output(["youtube-dl", "-J", "--flat-playlist", "--dateafter", "now+10week", youTubeMainPageURLs[page]]))
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
