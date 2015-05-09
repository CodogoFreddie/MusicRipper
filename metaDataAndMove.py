import subprocess
import os
import json

def printNested(thing, n):
	if type(thing) == type(["list"]):
		for thang in thing:
			printNested(thang, n+1)
	elif type(thing) == type({"dict": True}):
		for key in thing:
			print('\t'*n + key + ": ")
			printNested(thing[key], n+1)
	else:
		print('\t'*n + str(thing))

def addImagesToSongs(clasification):
	group = clasification[0]
	type_ = clasification[1]

	jsonFiles = [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and ".info.json" in f]

	for song in jsonFiles:
		try:
			basicInfo = getInfo(song)
		except:
			continue
		audioFileName = basicInfo[' ']
		info = addExtraTags(basicInfo, group, type_)

		sortOutImage(info["--ti"])

		shellShit(info, audioFileName, group)

def shellShit(info, audioFileName, group):
	subprocess.call(["mkdir", "-p", group])

	argsString = ["lame"]
	for key in info:
		argsString = argsString + [key, info[key]]

	argsString = argsString + [audioFileName] + [group + '/' + audioFileName]

	subprocess.call(argsString)
	subprocess.call(["rm", "-f", info["--ti"], audioFileName])
	subprocess.call(["rm", "-f", "*.json"])

def addExtraTags(info, group, type_):
	if type_ == "Genre":
		info["--tg"] = group

	elif type_ =="Curator":
		info["--tg"] = group
		info.pop("artist", None)

	elif type_ =="Artist":
		pass

	info.pop(" ", None)
	return info



def getInfo(jsonSRC):
	audioFormats = ["mp3", "ogg", "acc", "m4a"]
	imageFormats = ["jpg", "jpeg", "gif", "tff"]

	jsonFile = open(jsonSRC, 'r')
	jsonString = ""
	for line in jsonFile:
		jsonString += line
	jsonFile.close()
	decodedJson = json.loads(jsonString)

	info = {}
	info["--tt"] = decodedJson["title"]
	info["--ta"] = decodedJson["uploader"]

	audioFileName = []
	for format_ in audioFormats:
		# print(jsonSRC.replace(".info.json", '.' + format_))
		audioFileName.extend([ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and f == jsonSRC.replace(".info.json", '.' + format_) ])
		
	imageFileName = []
	for format_ in imageFormats:
		# print(jsonSRC.replace(".info.json", '.' + format_))
		imageFileName.extend([ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and f == jsonSRC.replace(".info.json", '.' + format_) ])
	
	info[' '] = audioFileName[0]
	info['--ti'] = imageFileName[0]

	return info

def sortOutImage(src):
	sizeString = subprocess.check_output(["convert", src, "-print", "Size: %wx%h\n", "/dev/null"]).decode("utf-8")
	(width, height) = map(lambda x: int(x), sizeString[:-1].replace("Size: ", '').split("x"))
	maxDim = max(width, height)
	minDim = min(width, height)
	ratio = maxDim / minDim
	scaleDownFactor = minDim / 500

	scaleWidth = str(int(width / scaleDownFactor))
	scaledHeight = str(int(height / scaleDownFactor))


	subprocess.call(["convert", src, "-scale", str(scaleWidth) + 'x' + str(scaledHeight), src])

	carvedWidth = min(scaleWidth, scaledHeight)
	carvedHeight = min(scaleWidth, scaledHeight)

	subprocess.call(["python2", "SeamCarving.py", str(src), str(src), str(carvedWidth), str(carvedHeight)])
