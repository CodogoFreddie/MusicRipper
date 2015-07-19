import database
import reddit
import youtube_dl
import metaDataAndMove
import os
import youtubeURLGrabber
import time
import sys

subReddits = []
subReddits.append( ("FutureSynth", "Genre") )
subReddits.append( ("FutureBass", "Genre") )
subReddits.append( ("Glitch", "Genre") )
subReddits.append( ("House", "Genre") )
subReddits.append( ("ElectroHouse", "Genre") )
subReddits.append( ("NewRetroWave", "Genre") )
subReddits.append( ("Outrun", "Genre") )
subReddits.append( ("Synthwave", "Genre") )

def gatherNewRedditURLs():
	global subReddits
	database.initDB()

	# download reddit urls
	for subReddit_ in subReddits:
		subReddit = subReddit_[0]
		print("getting urls for", subReddit)
		urlList = reddit.getHot(subReddit, 100) + reddit.getTopMonth(subReddit, 100)
		for url in urlList:
			database.addURL(url, subReddit_)

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
		ydl_opts['writeinfojson'] = 'True'

		try:
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
				metaDataAndMove.addImagesToSongs(group)
		except:
			database.markURLAsFucked(url, group)
			database.saveDB()
			continue;


		database.markURLAsClosed(url, group)
		database.saveDB()

		# os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
	if "-r" in sys.argv:
		gatherNewRedditURLs()

	if "-y" in sys.argv:
		youtubeURLGrabber.addYouTubeCuratorURLs()

	if "-u" in sys.argv:
		downloadURLs()

# downloadURLs()
