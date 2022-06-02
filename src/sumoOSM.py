import asyncio
import re
import config as conf
import jsonConfig as jc
import json
import os 
import shutil

async def sumoConvertOSM(fileName, filePath):


	newConfig = os.path.join(filePath, (fileName + ".sumocfg"))	
	sumoConfig = os.path.join(conf.gen["absPath"], conf.sumo["sumoConfig"])
	tripsScriptPath = os.path.join(conf.sumo["sumoPath"], conf.sumo["tripsScript"])
	tclScriptPath = os.path.join(conf.sumo["sumoPath"], conf.sumo["tclScript"])
	tripsAttempted = conf.sumo["tripsAttempted"]	

	convertOSM = f"netconvert --osm-files {fileName}.osm -o {fileName}.net.xml --no-warnings >> /dev/null"
	makeRoutes = f"{tripsScriptPath}  -n {fileName}.net.xml -r {fileName}routes.rou.xml -o {fileName}trips.xml -e {tripsAttempted}"
	makeTrace = f"sumo -c {fileName}.sumocfg --fcd-output {fileName}Trace.xml --no-warnings --no-step-log >> /dev/null"
	makeTcl = f"{tclScriptPath} --fcd-input {fileName}Trace.xml  --ns2mobility-output {fileName}.tcl >> /dev/null"

	try:
		shutil.copy(sumoConfig, newConfig)
	except: 
		print("error couldn't copy sumo config template")

	with open(newConfig, 'r') as f:
		data = f.read()
		data = data.replace("map", fileName)
		data = data.replace("routes", fileName + "routes")
	with open(newConfig, 'w') as f:
		f.write(data)
	
	os.chdir(filePath)	
	os.system(convertOSM)
	os.system(makeRoutes)
	os.system(makeTrace)
	os.system(makeTcl)

	tclFile = f"{fileName}.tcl"
	
	rex  = re.compile('node_\(.*?\)')
	with open(tclFile, 'r') as f:
		text = f.read()
		nodes = rex.findall(text)
		nodes = list(dict.fromkeys(nodes))
		numNodes = len(nodes) 
	jc.writeInfoJson(filePath)
	jc.writeToInfoJson("numOfNodes", numNodes, filePath)	
	os.chdir(conf.gen["absPath"])
