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

	i = 0
	for thing in database.nextURLToDownload():
		i = i + 3
		if i > 1:
			break
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
		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
			break

		imageLinker.addImagesToSongs(group)
		os.system('cls')


# gatherNewURLs()

downloadURLs()