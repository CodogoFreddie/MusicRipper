import database
import reddit
import youtube_dl
import imageLinker
import os

subReddits = ["FutureSynth", "FutureBass", "Glitch", "Trap", "House", "electrohouse"]
# subReddits = ["electrohouse"]

def gatherNewURLs():
	global subReddits
	database.initDB()

	# download reddit urls
	for subReddit in subReddits:
		print("getting urls for", subReddit)
		urlList = reddit.getHot(subReddit, 10)
		for url in urlList:
			database.addURL(url, subReddit)

		database.saveDB()

	# database.printDB()


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

		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])

			imageLinker.addImagesToSongs(group)

		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
			continue;

		database.markURLAsClosed(url, group)

		os.system('cls' if os.name == 'nt' else 'clear')


# gatherNewURLs()

downloadURLs()