import praw

r = praw.Reddit("Music URL harvester by /u/DrVonTrap")

def getHot(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_hot(limit=n):
		returnList = returnList + [submission.url]
		# print(submission.url)
		# print(submission.secure_media["oembed"]["provider_url"])
	return returnList

def getTopAll(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_all(limit=n):
		returnList = returnList + [submission.url]
	return returnList

def getTopWeek(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_week(limit=n):
		returnList = returnList + [submission.url]
	return returnList

def getTopMonth(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_all(limit=n):
		returnList = returnList + [submission.url]
	return returnList