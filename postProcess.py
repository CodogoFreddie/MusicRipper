import subprocess
import os
import json
import re

imageFileTypes = ["jpg", "png" "gif"]
audioFileTypes = ["m4a", "mp3", "flac", "aac", "vorbis", "opus","wav"]

def getFileNames():
	files = (subprocess.check_output(["ls", "Staging"]).decode('unicode_escape').split('\n'))
	infoFileName = ""
	audioFileName = ""
	thumbnailFileName = ""

	for file_ in files:
		if ".json" in file_:
			infoFileName = file_
		for type_ in imageFileTypes:
			if type_ in file_:
				thumbnailFileName = file_
		for type_ in audioFileTypes:
			if type_ in file_:
				audioFileName = file_

	return (infoFileName, thumbnailFileName, audioFileName)

def getMetaData(jsonFileName):
	jsonFile = open("Staging/" + jsonFileName, 'r')
	fuckPython3 = ""
	for line in jsonFile:
		fuckPython3 += line
	jsonFile.close()
	data = json.loads(fuckPython3)

	title = data["title"]
	uploader = data["uploader"]
	return {"title" : title, "uploader" : uploader}

def tryToAnaliseTitle(currentData):
	if re.match(".+ - .+", currentData["title"]):
		currentData["artist"] = currentData["title"].split(' - ')[0]
		currentData["title"] = currentData["title"].split(' - ')[1]
	return currentData

def squareifyImage(src):
	sizeString = subprocess.check_output(["convert", src, "-print", "Size: %wx%h\n", "/dev/null"]).decode("utf-8")
	(width, height) = map(lambda x: int(x), sizeString[:-1].replace("Size: ", '').split("x"))
	minDim = min(width, height)

	dimensions = str(minDim)+'x'+str(minDim)+"+0+0"

	subprocess.call(["convert", src, "-gravity", "center", "-crop", dimensions, src])

def tagify(metaData, group, thumbnailFileName):
	tags = {}
	print(group)

	if "artist" in metaData.keys():
		tags["--ta"] = metaData["artist"]
	else:
		tags["--ta"] = metaData["uploader"]

	if(group[1] == "Genre"):
		tags["--tg"] = group[0]
	elif(group[1] == "Curator"):
		tags["--tg"] = group[0]
	elif(group[1] == "Artist"):
		tags["--ta"] = group[0]

	tags["--tt"] = metaData["title"]

	tags["--ti"] = thumbnailFileName

	return tags

def combineAndProcess(folderName, fileName, tags):
	argsList = ["lame", "-h"]
	for key in tags.keys():
		argsList.extend([key, tags[key]])

	argsList.append("Staging/"+fileName)
	argsList.append(folderName+'/'+tags["--tt"]+'_'+fileName)

	print(' '.join(argsList))

	subprocess.call(["mkdir", folderName])
	subprocess.call(argsList)

def PostProcess(group):
	(infoFileName, thumbnailFileName, audioFileName) = getFileNames()
	metaData = getMetaData(infoFileName)
	metaData = tryToAnaliseTitle(metaData)
	squareifyImage("Staging/"+thumbnailFileName)
	tags = tagify(metaData, group, "Staging/"+thumbnailFileName)
	combineAndProcess(group[0], audioFileName, tags)
