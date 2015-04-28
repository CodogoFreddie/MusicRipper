import database
import reddit
import youtube_dl
import imageLinker
import os
import youtubeURLGrabber
import time

subReddits = ["FutureSynth", "FutureBass", "Glitch", "Trap", "House", "ElectroHouse", "NewRetroWave", "Outrun", "Synthwave"]
# subReddits = ["electrohouse"]

def gatherNewURLs():
	global subReddits
	database.initDB()

	# download reddit urls
	for subReddit in subReddits:
		print("getting urls for", subReddit)
		urlList = reddit.getHot(subReddit, 50) + reddit.getTopAll(subReddit, 100)
		for url in urlList:
			database.addURL(url, subReddit)

		database.saveDB()


def downloadURLs():
	database.initDB()

	for thing in database.nextURLToDownload():
		(group, url) = thing
		print('\t' + "trying to download", url, "to", group)
		ydl_opts = {}
		ydl_opts['format'] = 'bestaudio/best'
		ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
		ydl_opts['simulate']= False
		ydl_opts['writethumbnail'] = True
		ydl_opts['write_all_thumbnails'] = True
		ydl_opts['flat_playlist'] = True
		ydl_opts['extract_flat'] = 'in_playlist'
		ydl_opts['noplaylist'] = 'True'

		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				vals = ydl.download([url])
				print(vals)
			imageLinker.addImagesToSongs(group, ".mp3")

		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
			continue;

		database.markURLAsClosed(url, group)

		database.saveDB()
		os.system('cls' if os.name == 'nt' else 'clear')

# gatherNewURLs()
# downloadURLs()

youtubeURLGrabber.addYouTubeCuratorURLs()
# downloadURLs()