import yaml

validThings = []
validThings.append( ("FutureBass", "Genre") )
validThings.append( ("Glitch", "Genre") )
validThings.append( ("House", "Genre") )
validThings.append( ("ElectroHouse", "Genre") )
validThings.append( ("ArcticEmpire", "Curator") )
validThings.append( ("AirwaveMusic", "Curator") )
validThings.append( ("TrapCity", "Curator") )
validThings.append( ("MrSuicideSheep", "Curator") )
validThings.append( ("TheSoundYouNeed", "Curator") )
validThings.append( ("EOENetwork", "Curator") )
validThings.append( ("SummerBreeze", "Curator") )
validThings.append( ("BigDataBigData", "Artist") )
validThings.append( ("Pentatonix", "Artist") )

dbFile = open("download.db.1", 'r')
db = yaml.load(dbFile)
dbFile.close()

db2 = {}
db2["open"] = {}
db2["closed"] = {}
db2["fucked"] = {}

for thing in db["open"].keys():
	if thing in validThings:
		db2["open"][thing] = db["open"][thing] + db["closed"][thing] + db["fucked"][thing]
		db2["closed"][thing] = []
		db2["fucked"][thing] = []

print(db2)

dbFile = open("download.db.clean", 'w')
yaml.dump(db2, dbFile)
dbFile.close()