import database
import reddit
import youtube_dl
import metaDataAndMove
import os
import youtubeURLGrabber
import time
import sys

subReddits = ["FutureSynth", "FutureBass", "Glitch", "Trap", "House", "ElectroHouse", "NewRetroWave", "Outrun", "Synthwave"]
# subReddits = ["electrohouse"]

def gatherNewRedditURLs():
	global subReddits
	database.initDB()

	# download reddit urls
	for subReddit in subReddits:
		print("getting urls for", subReddit)
		# urlList = reddit.getHot(subReddit, 50) + reddit.getTopAll(subReddit, 100)
		urlList = reddit.getTopAll(subReddit, 1)
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
		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
			continue;

		metaDataAndMove.addImagesToSongs(group)

		database.markURLAsClosed(url, group)

		database.saveDB()
		# os.system('cls' if os.name == 'nt' else 'clear')

database.initDB()
database.reOpenAllClosed()
database.saveDB()

if __name__ == "__main__":
	if "-r" in sys.argv:
		gatherNewRedditURLs()

	if "-y" in sys.argv:
		youtubeURLGrabber.addYouTubeCuratorURLs()

	if "-u" in sys.argv:
		downloadURLs()

# downloadURLs()