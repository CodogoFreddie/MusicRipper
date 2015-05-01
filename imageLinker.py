import subprocess
import os

def addImagesToSongs(group, extension):
	audioFiles = [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and extension in f]

	artAndAudioTuple = list(map(lambda x: (x, x.replace(extension, ".jpg")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(extension, ".png")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(extension, ".tff")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(extension, ".bmp")), audioFiles))
	artAndAudioTuple = list(filter(lambda x: os.path.isfile(os.path.join(os.getcwd(),x[1])), artAndAudioTuple))
	# print(artAndAudioTuple)

	for tuple_ in artAndAudioTuple:
		print("converting", tuple_)
		subprocess.call(["lame", "--tg", str(tuple_[1]), "--tl", group, str(tuple_[0])])
		subprocess.call(["rm", str(tuple_[1]), str(tuple_[0])])

	subprocess.call(["mkdir", group, "-p"])

	packedAudioFiles = [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and extension*2 in f]

	for paf in packedAudioFiles:
		subprocess.call(["mv", paf, group + '/' + paf[:-4]])

	for file_ in audioFiles:
		subprocess.call(["mkdir", "Uncovered/" + group, "-p"])
		subprocess.call(["mv", file_, "Uncovered/" + group + '/' + file_[:-4]])


	# subprocess.call(["feh", ' '.join(artAndAudioTuple)])
