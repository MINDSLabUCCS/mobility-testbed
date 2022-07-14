import os
import subprocess
import time
import config as conf
import shutil
import asyncio
import csvReformat as rCSV

# /waf --run "ns2TraceInterface --configFile=/home/jason/testbedMultiproc/ns3/map_1NS3SimplifiedBuildings.json"


async def run(mapDirPath, dirName):
    ns3OutputFiles = [f"DlPdcpStats{dirName}.txt", f"DlRlcStats{dirName}.txt", f"packetFlowMonitor{dirName}.xml", f"Legend{dirName}.txt",
                      f"DlPhyTransmissionTrace{dirName}.txt", f"EnbSchedAllocTraces{dirName}.txt", f"RxPacketTrace{dirName}.txt", f"UlPdcpStats{dirName}.txt", f"UlRlcStats{dirName}.txt"]
    ns3OutputFilesCSV = [f"DlPdcpStats{dirName}.txt", f"DlRlcStats{dirName}.txt", f"DlPhyTransmissionTrace{dirName}.txt",
                         f"EnbSchedAllocTraces{dirName}.txt", f"RxPacketTrace{dirName}.txt", f"UlPdcpStats{dirName}.txt", f"UlRlcStats{dirName}.txt"]

    ns3OutputFileColumnLabels = ["Tx,Time,CellId,RNTI,LCID,packetSize,delay", "Tx,Time,CellId,RNTI,LCID,packetSize,delay",
                                 "", "", "", "Tx, Time, CellId, RNTI, LCID, packetSize, delay", f"Tx, Time, CellId, RNTI, LCID, packetSize,delay"]
    config = os.path.join(mapDirPath, "indivConfig.json")
    pythonDir = os.path.join(conf.gen["absPath"], "src")
    ns3Path = os.path.join(conf.gen["absPath"], conf.ns3["ns3Path"])
    ns3OutputDir = os.path.join(mapDirPath, (dirName + "_ns3"))
    progressFile = ("progress" + dirName + ".txt")
    progressCall = f"python /home/testbed/src/progress.py -i {progressFile} &"
# os.system(progressCall)
    os.chdir(ns3Path)
    print("running NS3 sim")
    call = f"./waf --run \"ns2TraceInterface --configFile={config} $NS3_JOB_ID\" >> /dev/null"
    d = dict(os.environ)
    d["NS3_JOB_ID"] = dirName
##    subprocess.Popen(call, shell=True, env=d).wait()
    proc = await asyncio.create_subprocess_shell(call, stdout=asyncio.subprocess.PIPE, shell=True, env=d)
    stdout, stderr = await proc.communicate()
    print("finished ns3 sim")
    os.mkdir(ns3OutputDir)
    print(os.listdir())
# os.remove(progressFile)
    print("beginning csv reformat")
    os.chdir(ns3Path)
    for count, x in enumerate(ns3OutputFiles):
        print(count)
        mapDirFolder = os.path.join(ns3OutputDir, x)
        shutil.copyfile(x, mapDirFolder, follow_symlinks=True)
        os.chdir(ns3OutputDir)
        rCSV.format(ns3OutputFilesCSV[count], ns3OutputFileColumnLabels[count])
        os.chdir(ns3Path)
    os.chdir(pythonDir)
