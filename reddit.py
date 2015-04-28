import praw
import html

r = praw.Reddit("Music URL harvester by /u/DrVonTrap")

def getHot(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_hot(limit=n):
		try:
			print(str('\t' + submission.url))
			if "reddit" not in submission.url:
				returnList = returnList + [submission.url]
		except:
			print("\turl is fucked")
			continue
	return returnList

def getTopAll(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_all(limit=n):
		try:
			print(str('\t' + submission.url))
			if "reddit" not in submission.url:
				returnList = returnList + [submission.url]
		except:
			print("\turl is fucked")
			continue
	return returnList

def getTopWeek(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_week(limit=n):
		try:
			print(str('\t' + submission.url))
			if "reddit" not in submission.url:
				returnList = returnList + [submission.url]
		except:
			print("\turl is fucked")
			continue
	return returnList

def getTopMonth(subReddit, n):
	global r
	subreddit = r.get_subreddit(subReddit)
	returnList = []
	for submission in subreddit.get_top_from_all(limit=n):
		try:
			print(str('\t' + submission.url))
			if "reddit" not in submission.url:
				returnList = returnList + [submission.url]
		except:
			print("\turl is fucked")
			continue
	return returnList