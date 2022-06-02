import os 
import math
import xml.etree.ElementTree as ET
import json
import config
import asyncio

def maxMin(dirName, mapDirPath):
    netFile = dirName + ".net.xml"
    netFilePath = os.path.join(mapDirPath, netFile)
    tree = ET.ElementTree(file=netFilePath)
    bounds = tree.find('./location').attrib['convBoundary']
    bounds = bounds.split(",")
    return bounds

def equidistant(x,y,num):
    pos = []
    xLarger = False;
    if(x >= y): 
        xLarger = True;
        shortRow = math.pow(num,(y/(y+x)))
    else:
        shortRow = math.pow(num,(x/(y+x)))

    intShortRow = math.ceil(shortRow)
    intLongRow = math.ceil(num/intShortRow)
    totalSlots = intShortRow*intLongRow
    diff = totalSlots%num

    for i in range(intLongRow):
        for u in range(intShortRow):
            indivPos = []
            if xLarger == False:
                indivPos.append(((x/intShortRow)*u)+((x/intShortRow)/2))
                indivPos.append(((y/intLongRow)*i)+((y/intLongRow))/2)
            else:   
                indivPos.append(((x/intLongRow)*i)+((x/intLongRow))/2)
                indivPos.append(((y/intShortRow)*u)+((y/intShortRow)/2))
            if len(pos) <= num:
                pos.append(indivPos)
                continue
            break       
        if(len(pos) == num):
            return pos

        while(len(pos) > num):
            pos.pop()
            if(len(pos) == num):
                return pos
        if(len(pos) < num):
            print("error: enb.py generated fewer coordinates than enb's requested")
            print("this shouldn't ever happen; so if it does probably logic error")
            exit()

async def enbPlacement(mapDirPath, dirName): 
    enbNum = config.ns3["enbNum"]
    onInterval = config.ns3["onInterval"]
    interval = config.ns3["interval"]
    enbJson = os.path.join(mapDirPath,"enb.json")
    bounds = maxMin(dirName, mapDirPath)
    pos = []
    if(onInterval == True):         
        gridX = bounds[2] / interval    
        gridY = bounds[3] / interval
        for x in range(gridX):
            for y in range(gridY):
                indivPos = []
                indivPos.append(x * gridX)
                indivPos.append(y * gridY)
                pos.append(indivPos)    
    else:
        pos = equidistant(float(bounds[2]),float(bounds[3]),enbNum)

    with open(enbJson, "w") as f:
        f.write(json.dumps(pos))
