from tqdm import tqdm
import asyncio
import os
import time
import re
import config
import sys, getopt

printQueue = []
progressQueue = []


def openReadCloseReturn(fileName):
        with open(fileName, "r") as f:
                line = f.readline()
                f.close()
        return line

def extractFloat(string):
        return re.findall("\d+\.\d+", string)

def ns3(progressFile):
	progressPath = os.path.join("/home/testbed/ns3/ns3-mmwave-antenna",progressFile) 
	stagnant = 0
	lastFloat = 0.0
	time.sleep(10)

	i = float(extractFloat(openReadCloseReturn(progressPath))[0])/10**9
	while(True):
		current = extractFloat(openReadCloseReturn(progressPath))
		if(len(current) == 0):
			break
		if (float(current[0]) == 0):
			break
		if (stagnant == 3):	
			print(progressFile + ": error stagnant exiting...")
			break
		currentFloat = (float(current[0])/10**8)
		timeLeft = (config.ns3["simTime"] - currentFloat)
		if (timeLeft < 0.1):
			print(progressFile + ": finishing...")
			break
		if (currentFloat == lastFloat):
			stagnant = stagnant + 1
			time.sleep(5)
			continue
		time.sleep(5)
		stagnant = 0
		lastFloat = currentFloat
		print(progressFile + ": " + str(currentFloat) + "/" + str(config.ns3["simTime"]) + "s")
		i += ((currentFloat)-i)

def main(argv):
	progressFile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["progfile="])
	except getopt.GetoptError:
		print ('progress.py -i <progressFile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('progress.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--progFile"):
			progressFile = arg
	ns3(progressFile)

if __name__ == "__main__":
   main(sys.argv[1:])
