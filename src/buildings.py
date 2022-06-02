import asyncio
import os
import xml.etree.ElementTree as ET
import json 
import polyplot

heightIndicatorTags = ["isced:level", "level", "height", "floors"]

def maxMin(arr):
	maxArr = arr[0]
	minArr = arr[0]
	for x in arr:
		if maxArr < x:
			maxArr = x
		if minArr > x:
			minArr = x 
	return (maxArr, minArr)

def simplify(arr): 
	x = (arr[::2])  ##x values
	y = (arr[1::2]) ##y values
	xMaxMin = maxMin(x)
	yMaxMin = maxMin(y)
	simplebuilding = [xMaxMin[0], xMaxMin[1], yMaxMin[0], yMaxMin[1]] 
	return simplebuilding;

def polyParse(buildingsComplex, NS3SimplifiedBuildings):
	buildingsSimplified = []
	for x in buildingsComplex:
		buildingsSimplified.append(simplify(x))	 
	with open(NS3SimplifiedBuildings, 'a') as f:
                        f.write(json.dumps(buildingsSimplified))

def coordinate(latlonglength, latlonglow, xyhigh, coordinate):
	return (xyhigh * (abs(coordinate - latlonglow)/latlonglength))

def readthrough(latlength, lowlat, longlength, lowlong, highx, highy, tmpBuildings, buildings, NS3SimplifiedBuildings):
	buildingsArr = []
	with open(tmpBuildings, "r") as read_file:
		jsonList = json.load(read_file)
		for x in jsonList:
			buildingDem = []
			for key,values in x.items():
				if(key != "levels"):
					buildingDem.append(coordinate(longlength, lowlong, highy, float(values[0])))
					buildingDem.append(coordinate(latlength, lowlat, highx, float(values[1])))
					
			buildingsArr.append(buildingDem)
		polyParse(buildingsArr, NS3SimplifiedBuildings)	
		with open(buildings, 'a') as f:
			f.write(json.dumps(buildingsArr))
			

def convert(latlongTuple,xyTuple,buildings, tmpBuildings, NS3SimplifiedBuildings):
	latlong = [float(ele) for ele in list(latlongTuple)]	
	xy = [float(ele) for ele in list(xyTuple)]	
	
	lowlat = latlong[0]
	highlat = latlong[2]
	lowlong = latlong[1]
	highlong = latlong[3]
	highx = xy[2]
	highy = xy[3]
	
	latlength = abs(highlat - lowlat)
	longlength = abs(highlong - lowlong)
	
	readthrough(latlength, lowlat, longlength, lowlong, highx, highy, tmpBuildings, buildings, NS3SimplifiedBuildings)

def parseOsmFile(osmFile, tmpBuildings):
	tree = ET.parse(osmFile)
	root = tree.getroot()
	jsonArr = []
	for way in root:
		if(way.tag == "way"):
			for tags in way:
				if(tags.tag == "tag"):
					if (tags.attrib['k'] == "building"): 
						buildingDict = {}
						for buildingTags in way:
							if (buildingTags.tag == "nd"):
								for node in root: 
									if (node.attrib['id'] == buildingTags.attrib['ref']):
										coordinates = [node.attrib['lat'],node.attrib['lon']]
										buildingDict[node.attrib['id']]=coordinates
							for x in heightIndicatorTags:
								if (buildingTags.tag == "tag" and  buildingTags.attrib['k'] == x):
									buildingDict["levels"] = buildingTags.attrib['v']
						jsonArr.append(json.dumps(buildingDict))
	with open(tmpBuildings, 'a') as f:
		f.write("[\n")
		for x in jsonArr[:-1]:
			f.write(x)
			f.write(",\n")
		f.write(jsonArr[-1])
		f.write("\n]")


def parseNetFile(netFile, buildings, tmpBuildings, NS3SimplifiedBuildings):
	tree = ET.ElementTree(file=netFile)    
	newBounds = tree.find('./location').attrib['convBoundary']
	newBounds = newBounds.split(",")
	oldBounds = tree.find('./location').attrib['origBoundary']
	oldBounds = oldBounds.split(",")
	convert(oldBounds, newBounds, buildings, tmpBuildings, NS3SimplifiedBuildings)

async def parse(dirName, mapDirPath):

	osmFile = dirName + ".osm"
	netFile = dirName + ".net.xml"
	
	buildings = os.path.join(mapDirPath, (dirName + "Buildings.json"))
	NS3SimplifiedBuildings = os.path.join(mapDirPath, "NS3SimplifiedBuildings.json")
	tmpBuildings = os.path.join(mapDirPath, "tmpBuildings.json")
	osmFilePath = os.path.join(mapDirPath, osmFile)
	netFilePath = os.path.join(mapDirPath, netFile)
	
	parseOsmFile(osmFilePath, tmpBuildings)
	parseNetFile(netFilePath, buildings, tmpBuildings, NS3SimplifiedBuildings)
	os.remove(tmpBuildings)
