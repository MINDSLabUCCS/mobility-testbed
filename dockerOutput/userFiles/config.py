import os
import datetime

gen = {

    "absPath": "/home/testbed",  # the absolute path to the python venv
    "userDir": "userFiles",  # the directory with the geoCSV and where finished outputs go
    "outputDir": "outputMaster/output",
    "concurrencyMult": 1,  # os.cpu_count()/2, ##pretty conservative for default

    # currently unused, for moving files to and from docker vs host system
    "hostOutputDir": "output",
    "infoFilePath": "src/templates/info.py",
    "templateJsonPath": "src/templates/templateNS3.json"

}

osm = {

    "mapFile": "colorado.osm.pbf",
    "geoCSV": ("denver.csv"),  # csv file with lat long coordinates
    "geoSideLen": 1,  # the side length of a square area centered on the lat long given
    "csvHeader": False,
    "latLongFormat": True  # whether the coordinates in the csv are latLong, false = longLat

}

sumo = {

    # params
    "tripsAttempted": "10",
    "sumoPath": "/usr/share/sumo",
    "tripsScript": "tools/randomTrips.py",
    "tclScript": "tools/traceExporter.py",

    # defaults
    "sumoConfig": "src/templates/simple.sumocfg"


    # override defaults
    # "overRideOptions" : False,

}

ns3 = {

    # paths
    "ns3BuildOptions": "./waf build",
    "ns3Path": "ns3/ns3-mmwave-antenna/",
    "scriptPath": "/home/testbed/ns3/ns3-mmwave-antenna/scratch/ns3TraceInterface.cc",
    "scriptName": "ns2TraceInterface",

    # simulation parameters

    # simulation time in seconds
    "simTime": 2,

    # network Params
    "bandDiv": 2,
    "frequency": 28e9,  # center frequency
    "totalBandwidth": 800e6,
    "dataRate": "100Gb/s",
    "mtu": 1500,
    "delay": 0.010,  # intra-packet delay
    "useCa": False,

    # Antenna
    "ueCodeBook": 22,  # rows and columns 22 -> 2 Rows 2 Columns, 84 -> 8 rows 2 Columns, etc
    # (note available codebooks: testbedMultiproc/ns3/ns3-mmwave-antenna/src/mmwave/model/Codebooks)
    "enbCodeBook": 22,

    # eNodeB Params
    "onInterval": False,  # if True enbs will be place on a grid every interval
    "interval": 0.0,  # interval in meters
    "enbNum": 2,
    "enbHeight": 15,  # meters

    # Building Params
    "type": "Building::Residential",
    "material": "Building::ConcreteWithWindows",
    "roomsX": 1,
    "roomsY": 1,
    "floors": 1,
    "buildingHeight": 5.0  # meters
}
