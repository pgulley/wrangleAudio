#Parser for .caf audio files. 
#This is unique to the "Apple Loops" included in Garage band and yeilds 1157 file/tag pairs
import os
from itertools import izip
import json

fileLocation = "./LoopsAndTags/"

#this creates a file with a map of all of the relevant meta data to the filename.
def generateFileMap():
	output = open("tags.txt", "w")
	allDescs = []
	for filename in os.listdir(fileLocation):
		a = open(fileLocation+filename, 'r').read()
		b = a.split("uuid")[1].split("\x00")
		#sound effect files have a different format going on that we don't like.
		if "Sound Effect" in b:
			pass

		if "time signature" not in b:
			pass

		else:
			#remove non-printable data
			b.pop(7)
			b = filter(None, b)
			b[0] = b[0][1:]
			i = iter(b)
			tagdict = dict(izip(i, i))

			#handfull of files also lack descriptors for some reason. throw them out.
			if tagdict['genre'] == "descriptors":
				pass
			else:
				tagdict["descriptors"] = tagdict["descriptors"].split(",")
				fileAndTags = {"name":filename,
							   "tags":tagdict}
				output.write(str(fileAndTags)+"\n")
	output.close();
	
def allDescriptors():
	#Generates descriptorList
	a = open("tags.txt")
	allDescs = {}
	for line in a:
		line = eval(line)
		desc = line["tags"]["descriptors"]
		for d in desc:
			if d not in allDescs:
				allDescs[d] = 1
			else:
				allDescs[d] = allDescs[d]+1
	c = open("allDescs.txt", "w")
	c.write(str(allDescs))
	c.close()

def descHash():
	allDescsFile = open("allDescs.txt", "r")
	allDescs = sorted(eval(allDescsFile.read()).keys())
	allDescsFile.close()
	tags = open("tags.txt", "r")
	tagHash = open("hash.txt", "w")
	for line in tags:
		line = eval(line)
		desc = line["tags"]["descriptors"]
		descHash = []
		for d in desc:
			num = allDescs.index(d)
			descHash.append(num)
		simpleHash = {"file":line["name"],
					  "tags":descHash}
		tagHash.write(str(simpleHash)+"\n")
	tagHash.close()
	tags.close()




if __name__ == "__main__":
	generateFileMap()
	allDescriptors()
	descHash()

##TO DO:
## create spectrograms for each file 
## determine 'chip size' and scale spectrograms. 


