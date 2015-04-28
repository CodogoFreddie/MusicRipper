import yaml

db = {}

def initDB():
	global db
	dbFile = open("download.db", 'r')
	db = yaml.load(dbFile)
	if db == None:
		db = {"open": dict([]), "closed": dict([]), "fucked": dict([])}

	dbFile.close()

def nextURLToDownload():
	global db
	for group in db["open"]:
		while len(db["open"][group]) > 0:
			yieldURL = db["open"][group][0]
			yield (group, yieldURL)
			db["open"][group] = db["open"][group][1:]

def ensureGroupExists(group):
	global db
	if group not in db["open"].keys():
		db["open"][group] = []
	if group not in db["closed"].keys():
		db["closed"][group] = []
	if group not in db["fucked"].keys():
		db["fucked"][group] = []

def addURL(urlString, group):
	global db
	ensureGroupExists(group)
	if urlString in db["open"][group]:
		print('\t' + "allready marked to download", urlString)
	elif urlString in db["closed"][group]:
		print('\t' + "allready downloaded", urlString)
	elif urlString in db["fucked"][group]:
		print('\t' + "link is fucked", urlString)
	else:
		db["open"][group].append(urlString)

def markURLAsClosed(urlString, group):
	global db
	ensureGroupExists(group)
	if urlString in db["open"][group]:
		db["open"][group].remove(urlString)
		db["closed"][group].append(urlString)
	elif urlString in db["closed"][group]:
		print('\t' + "allready downloaded", urlString)
	elif urlString in db["fucked"][group]:
		print('\t' + "link is fucked", urlString)
	else:
		print('\t' + "not marked for downloading", urlString)

def markURLAsFucked(urlString, group):
	global db
	ensureGroupExists(group)
	if urlString in db["open"][group]:
		db["open"][group].remove(urlString)
		db["fucked"][group].append(urlString)
		print('\t' + "marked as fucked", urlString)
	elif urlString in db["closed"][group]:
		print('\t' + "allready downloaded", urlString)
	elif urlString in db["fucked"][group]:
		print('\t' + "allready marked as fucked", urlString)
	else:
		print('\t' + "not marked for downloading", urlString)

def saveDB():
	global db
	dbFile = open("download.db", 'w')
	yaml.dump(db, dbFile)
	dbFile.close()

def printDB():
	global db
	print('\t' + db)

