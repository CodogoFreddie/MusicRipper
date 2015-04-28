import subprocess
import os

def addImagesToSongs(group):
	audioFiles = [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and ".mp3" in f]

	artAndAudioTuple = list(map(lambda x: (x, x.replace(".mp3", ".jpg")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(".mp3", ".png")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(".mp3", ".tff")), audioFiles))
	artAndAudioTuple = artAndAudioTuple + list(map(lambda x: (x, x.replace(".mp3", ".bmp")), audioFiles))
	artAndAudioTuple = list(filter(lambda x: os.path.isfile(os.path.join(os.getcwd(),x[1])), artAndAudioTuple))
	# print(artAndAudioTuple)

	for tuple_ in artAndAudioTuple:
		print("converting", tuple_)
		subprocess.call(["lame", "--ti", str(tuple_[1]), str(tuple_[0])])
		subprocess.call(["rm", str(tuple_[1]), str(tuple_[0])])

	subprocess.call(["mkdir", group, "-p"])

	packedAudioFiles = [ f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),f)) and ".mp3.mp3" in f]

	for paf in packedAudioFiles:
		subprocess.call(["mv", paf, group + '/' + paf[:-4]])

	for file_ in audioFiles:
		subprocess.call(["mkdir", "Uncovered/" + group, "-p"])
		subprocess.call(["mv", file_, "Uncovered/" + group + '/' + file_[:-4]])


	# subprocess.call(["feh", ' '.join(artAndAudioTuple)])
