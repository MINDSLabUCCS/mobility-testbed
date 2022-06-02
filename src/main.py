import asyncio
import datetime
import linecache
import shutil
##from tqdm import tqdm, trange 
import glob, os
import pandas as pd

##import functions
import geoArea
import extractOSM
import sumoOSM
import buildings
import config
import polyplot
import runNS3 as ns3
import jsonConfig as jc
import enb
conf = config

##output directory time/date stamp
now = datetime.datetime.now()
format = "_%H-%M-%S_on_%d.%m.%Y"
conf.gen["outputDir"] = conf.gen["outputDir"] + now.strftime(format)

def mkdir(mapDirPath, geoLine):
	os.mkdir(mapDirPath)		
	infoPath = os.path.join(conf.gen["absPath"],conf.gen["infoFilePath"])

def doCleanUp():
	ns3Path = os.path.join(conf.gen["absPath"], conf.ns3["ns3Path"])
	os.chdir(ns3Path)
	for f in glob.glob("*.txt"):
		os.remove(f)

async def task(count):
	csvPath = os.path.join(conf.gen["absPath"], conf.gen["userDir"], conf.osm["geoCSV"])
	line = linecache.getline(csvPath, count)	
	if not line:
		return
	if line.find("\n"):
		line = line.replace("\n", "")
	coordinates = geoArea.calc(line)
	dirName = ("map_"+str(count))	
	mapDirPath = os.path.join(conf.gen["absPath"], conf.gen["outputDir"], dirName)
	print(mapDirPath)
	print("task " + str(count) + line + ": making map directory")
	mkdir(mapDirPath, line)		
	print("task " + str(count) + line + ": extracting OSM")
	await extractOSM.extract(mapDirPath, coordinates)
	print("task " + str(count) + line + ": running sumo sim")
	await sumoOSM.sumoConvertOSM(dirName, mapDirPath)
	print("task " + str(count) + line + ": getting buildings")
	await buildings.parse(dirName, mapDirPath)	
	print("task " + str(count) + line + ": placing enbs")
	await enb.enbPlacement(mapDirPath, dirName)
	print("task " + str(count) + line + ": ns3JsonConfig")
	await jc.jsonIndivConfig(mapDirPath, dirName)	
	print("task " + str(count) + line + ": running ns3 sim")
	await ns3.run(mapDirPath, dirName)
	print("task " + str(count) + line + ": done")

async def main():  

	csvPath = os.path.join(conf.gen["absPath"], conf.gen["userDir"], conf.osm["geoCSV"])
	csv = pd.read_csv(csvPath); 		
	outputPath = os.path.join(conf.gen["absPath"],conf.gen["outputDir"])
	numMap = len(csv)	
	concurrencyMult = conf.gen["concurrencyMult"]	
	mapTasks = set()

	os.mkdir(outputPath)	
	jc.jsonMasterConfig()	
	if(conf.osm["csvHeader"] == True): 
		numMaps = numMaps - 1

	for i in range(numMap):
		if len(mapTasks) >= concurrencyMult:
			# Wait for map(extraction, sumo) proccessing 
			try:
				_done, mapTasks = await asyncio.wait(mapTasks, return_when=asyncio.FIRST_COMPLETED)
			except asyncio.CancelledError:
				doCleanUp()
				return 1; 
		mapTasks.add(asyncio.create_task(task(i)))
	# Wait for the remaining maps to finish
	await asyncio.wait(mapTasks)

asyncio.run(main())
