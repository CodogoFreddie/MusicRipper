import database
import reddit

subReddits = ["FutureSynth", "FutureBass", "Glitch", "Trap", "House", "ElectroHouse"]
# subReddits = ["FutureSynth"]

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

gatherNewURLs()