import yaml
import subprocess

db = {}

def initDB():
	global db
	for i in range(2,7):
		try:
			dbFile = open("download.db." + str(i), 'r')
			db = yaml.load(dbFile)
			dbFile.close()
			break
		except:
			continue
	if len(db) == 0:
		db = {"open": dict([]), "closed": dict([]), "fucked": dict([])}

def nextURLToDownload():
	global db
	while True:
		for group in db["open"]:
			if len(db["open"][group]) > 0:
				yieldURL = db["open"][group][0]
				yield (group, yieldURL)
				db["open"][group] = db["open"][group][1:]
			else:
				anyLeft = False
				for group in db["open"]:
					if len(db["open"][group]) > 0:
						anyLeft = True
				if anyLeft:
					continue
				else:
					return

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

def reOpenAllClosed():
	global db
	# print(db)
	for group in db["closed"]:
		for item in db["closed"][group]:
			print(item)
			db["closed"][group].remove(item)
			db["open"][group].append(item)
	
			

def saveDB():
	global db
	subprocess.call(["cp", "download.db.5", "download.db.6"])
	subprocess.call(["cp", "download.db.4", "download.db.5"])
	subprocess.call(["cp", "download.db.3", "download.db.4"])
	subprocess.call(["cp", "download.db.2", "download.db.3"])
	subprocess.call(["cp", "download.db.1", "download.db.2"])
	dbFile = open("download.db.1", 'w')
	yaml.dump(db, dbFile)
	dbFile.close()

def printDB():
	global db
	print('\t' + db)

