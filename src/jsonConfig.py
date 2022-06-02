import json
import os
import config
import asyncio 

info = {
"coordinates": "",
"path": "",
"numOfNodes": 0
}

def writeInfoJson(mapDirPath):  
        path = os.path.join(mapDirPath, "info.json")    
        with open(path,"w") as f:
                f.write(json.dumps(info))
                f.close()

def writeToInfoJson(insertKey, insertValue, mapDirPath):
	tmpInfo = info 
	infoPath = os.path.join(mapDirPath, "info.json")
	 
	with open(infoPath, "r") as f:
		jFile = json.load(f)
		for key, value in jFile.items():
			if key != insertKey:
				tmpInfo[key] = value            
				continue
			tmpInfo[key] = insertValue
		f.close()

	with open(infoPath, "w") as f:
		f.write(json.dumps(tmpInfo))
		f.close()

async def jsonIndivConfig(mapDirPath, dirName):
	masterConfigJson = os.path.join(config.gen["absPath"], config.gen["outputDir"], "ns3Config.json")
	simpleBuildings = os.path.join(mapDirPath, "NS3SimplifiedBuildings.json")
	infoJson = os.path.join(mapDirPath, "info.json")
	indivConfig = os.path.join(mapDirPath, "indivConfig.json")
	enbPos = os.path.join(mapDirPath, "enb.json")
	
	with open(infoJson, "r") as f: ##info json 
		jsonInfo = json.load(f)
		nodeNum = jsonInfo["numOfNodes"]
	with open(simpleBuildings, "r") as f: ##buildings 
		jsonBuildings = json.load(f) 	
		f.close()
	with open(enbPos, "r") as f: ## for enb placement 
		jsonEnb = json.load(f)
		f.close()
	with open(masterConfigJson,"r") as f: ## master config
		tmpConfigJson = json.load(f)
		f.close()

	tmpConfigJson["buildings"]["coordinates"] = jsonBuildings
	tmpConfigJson["ns3Params"]["nodeNum"] = nodeNum
	tmpConfigJson["enbs"]["coordinates"] = jsonEnb
	tmpConfigJson["enbs"]["enbNum"] = config.ns3["enbNum"]
	tcl = os.path.join(mapDirPath, (dirName + ".tcl"))
	tmpConfigJson["ns3Params"]["traceFile"] = tcl
	
	with open(indivConfig, "w") as f:
		f.write(json.dumps(tmpConfigJson))
		f.close()

def jsonMasterConfig():
	templatePath = os.path.join(config.gen["absPath"], config.gen["templateJsonPath"])
	masterConfigJson = os.path.join(config.gen["absPath"], config.gen["outputDir"], "ns3Config.json")
	
	with open(templatePath, "r") as readfile:
		jsonFile = json.load(readfile) 

	tmpJson = jsonFile
	conf = config.ns3

	for confkey, confvalue in conf.items():
		for jkey, jvalue in tmpJson["ns3Params"].items():
			if(jkey == confkey):
				tmpJson["ns3Params"][jkey] = confvalue

	with open(masterConfigJson,"w") as f:
		f.write(json.dumps(tmpJson))
		f.close()
