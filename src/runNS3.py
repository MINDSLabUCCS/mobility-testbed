import os
import subprocess
import time
import config as conf
import shutil
import asyncio 

##/waf --run "ns2TraceInterface --configFile=/home/jason/testbedMultiproc/ns3/map_1NS3SimplifiedBuildings.json"

async def run(mapDirPath, dirName): 	
	ns3OutputFiles = [f"DlPdcpStats{dirName}.txt",f"DlRlcStats{dirName}.txt",f"packetFlowMonitor{dirName}.xml",f"Legend{dirName}.txt",f"DlPhyTransmissionTrace{dirName}.txt",f"EnbSchedAllocTraces{dirName}.txt",f"RxPacketTrace{dirName}.txt",f"UlPdcpStats{dirName}.txt",f"UlRlcStats{dirName}.txt"]
	config  = os.path.join(mapDirPath, "indivConfig.json")
	pythonDir = os.path.join(conf.gen["absPath"],"src")
	ns3Path = os.path.join(conf.gen["absPath"], conf.ns3["ns3Path"])
	ns3OutputDir = os.path.join(mapDirPath, (dirName + "_ns3"))
	progressFile = ("progress" + dirName + ".txt")
	progressCall = f"python /home/testbed/src/progress.py -i {progressFile} &"
##	os.system(progressCall)
	os.chdir(ns3Path)	
	call = f"./waf --run \"ns2TraceInterface --configFile={config} $NS3_JOB_ID\" >> /dev/null"
	d = dict(os.environ)
	d["NS3_JOB_ID"] = dirName
##	subprocess.Popen(call, shell=True, env=d).wait()
	proc = await asyncio.create_subprocess_shell(call, stdout=asyncio.subprocess.PIPE, shell=True, env=d)
	stdout,stderr = await proc.communicate()
	os.mkdir(ns3OutputDir)	
	os.remove(progressFile)
	for x in ns3OutputFiles:	
		mapDirFolder = os.path.join(ns3OutputDir, x) 
		shutil.copyfile(x, mapDirFolder, follow_symlinks=True)
		os.remove(x)
	os.chdir(pythonDir)
