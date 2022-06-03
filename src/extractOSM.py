import os
import subprocess
import time
import config as conf
import asyncio 

async def extract(outputDir, coordinates):
	path = os.path.join(outputDir, "map_"+os.path.basename(outputDir).split("_")[1]+".osm")
	mapFile = os.path.join(conf.gen["absPath"], conf.gen["userDir"], conf.osm["mapFile"])
	coordinates = coordinates.replace('\n','')
	call = f'osmium extract -b {coordinates} {mapFile} --strategy=smart -o {path} >> /dev/null'
	proc = await asyncio.create_subprocess_shell(call, stdout=asyncio.subprocess.PIPE)
	stdout,stderr = await proc.communicate()
	return stdout
