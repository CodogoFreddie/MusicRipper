import subprocess
import os
import SeamCarving

def addImagesToSongs(group):
	audioFormats = ["mp3", "ogg", "acc", "m4a"]
	imageFormats = ["jpg", "jpeg", "gif", "tff"]

	audioFiles = []
	for format_ in audioFormats:
		audioFiles = audioFiles + [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and '.' + format_ in f]

	audioImagePairs = []
	for audioFile in audioFiles:
		for audioFormat in audioFormats:
			for imageFormat in imageFormats:
				if audioFormat in audioFile:
					imageFile = audioFile.replace(audioFormat, imageFormat)
					if os.path.isfile(os.path.join(os.getcwd(), imageFile)):
						audioImagePairs.append((audioFile, imageFile))
					else:
						audioImagePairs.append((audioFile, None))

	print(audioFiles)
	print(audioImagePairs)

	for pair in audioImagePairs:
		if pair[1] != None:
			sizeString = subprocess.check_output(["convert", pair[1], "-print", "Size: %wx%h\n", "/dev/null"]).decode("utf-8")
			print(sizeString)
			(width, height) = map(lambda x: int(x), sizeString[:-1].replace("Size: ", '').split("x"))
			maxDim = max(width, height)
			minDim = min(width, height)
			ratio = maxDim / minDim
			scaleDownFactor = minDim / 500

			if scaleDownFactor < 1:
				scaleWidth = minDim
				scaledHeight = minDim
			else:
				scaleWidth = str(int(width / scaleDownFactor))
				scaledHeight = str(int(height / scaleDownFactor))


			subprocess.call(["convert", pair[1], "-scale", scaleWidth + 'x' + scaledHeight, pair[1]])

			carvedWidth = min(scaleWidth, scaledHeight)
			carvedHeight = min(scaleWidth, scaledHeight)

			subprocess.call(["python2", "SeamCarving.py", str(pair[1]), str(pair[1]), str(carvedWidth), str(carvedHeight)])

			subprocess.call(["mkdir", "-p", group])
			subprocess.call(["lame", "--ti", pair[1], "--tg", group, pair[0]])
		else:
			subprocess.call(["mkdir", "-p", "Uncovered/" + group])
			subprocess.call(["lame", "--tg", group, pair[0]])


	#", "subprocess.call(["feh", ' '.join(artAndAudioTuple)])


#  convert in.jpg -print "Size: %wx%h\n" /dev/null 