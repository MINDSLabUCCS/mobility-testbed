## Mobility Testbed

#### A mmWave mobility simulator combining [Open Street Map](https://www.openstreetmap.org), [NS3](https://www.nsnam.org), and [SUMO](https://sumo.dlr.de/docs/index.html)
<br>

### Setting up the testbed docker image
 <br>

1. Install [Docker](https://www.docker.com)

2. Pull the testbed image:
 
     ```docker pull jcuthbert/mobility-testbed```

3. locate the "dockerOutput" folder this will be where the simulator outputs; also within it is a "userFiles" folder where the simulator will pull the configuration files. Below is an example of the three input files for the testbed: 

     * `config.py` is provided in the userFiles folder and can be edited to change simulation parameters

     * `yourMap.osm.pbf` file is an open street map file, information on downloading map segments can be found [here](https://wiki.openstreetmap.org/wiki/Downloading_data)

     * `yourCoordinates.csv` contains lat long coordinates on each line that define areas to cut out of the .osm.pbf file; default format is "`lat long (newline) lat long`" however this can be configured in `config.py`

          <img src="docs/userFilesExample.png" alt="docs/userFilesExample.png" width="600"/>

4. once you have configured the simulation you want to run and gotten the map and the coordinates you can use the following command to start the docker image; which will enter you into an interactive shell with its own "file system". The -v option is creating a local volume; which links your dockerOutput folder to the /home/testbed/outputMaster directory in the container.

     ```
     docker container run --interactive --tty  -v ..YOUR-PATH../dockerOutput:/home/testbed/outputMaster jcuthbert/mobility-testbed:latest /bin/bash
     ```

5. At this point the container should be running; run the following commands to activate the python virtual environment and begin the simulation. Note: if you want to edit your `config.py` simulation parameters while the image is running edit `/home/testbed/src/config.py` within the containers interactive shell. 

     ``` 
     source ./bin/activate
     python src/main.py
     ```

6. The simulation should begin; with status messages on the command line. As it runs output files and intermediatry files such as the SUMO route files will begin being generated in the `dockerOutput` shared volume. Each time you begin the simulation a new timestamped subfolder will be created. 

     <img src="docs/outputExample.png" alt="docs/outputExample.png" width="700"/>

     Although a different version of the ns3-mmwave than used in the simulator [this](https://github.com/nyuwireless-unipd/ns3-mmwave/wiki/ns3-mmWave-traces) is a helpful page for understanding the ns3 output files. 

<br>

### Building the dockerfile

(instructions in progress)