# testbed-dockerize
A mobility simulator using ns3, sumo, and Open Street Map, to create datasets 

There should be a .tar file and a folder named:

- testbed-standalone.tar
- dockerfile-source

testbed-standalone.tar:

Description:  
This is a docker image, it is labeled standalone because instead of seeking input for the OSM file, coordinates, and configuration        files, versions of these were "baked" into the image. This was done so that while we are testing we don't have to worry about sourcing those things.

Instructions to run: 
  1. Install docker: this can be done either at their website: https://www.docker.com or via a package manager like "apt"
  2. Import the .tar file to docker: https://docs.docker.com/engine/reference/commandline/image_import/
  3. To run the image use the following command: 
    docker run --interactive --tty  -v {the file path where you want the output to go} testbed.app:latest /bin/bash
  4. This will run the container starting a bash shell, (sort of like you are ssh'ed into the docker image)
  5. your path should be: /home/testbed, if it is then run: " source ./bin/activate " this activates the python venv
  6. then cd to " /home/testbed/src " this is the python src directory
  7. To test the simulator run: python main.py, this will start the simulator with defaults 
  8. (if you wish to change parameters you can edit the " config.py " file or the ns3 program at: " ns3/ns3-mmwave-   antenna/scratch/ns2TraceInterface.cc "

dockerfile-source: 

Description: 
This folder contains the dockerfile for creating a docker image. Additional files/directories in the same directory as the dockerfile are needed in order to build it: (NOTE: the large OSM PBF file has been ommitted from the "userFiles" directory due to its large size, this is not required to test building the file but is to run the testbed itself)

- "ns3"               the ns3-mmwave standalone with the testbed ns3 program 
- "userFiles"         the Open Street Map file and the coordinates supplied by the user to simulate with (see changes below)
- "src"               the python files for the testbed
- "requirements.txt"  the python dependencies that will be installed when building the dockerfile

Instructions to build: 

see documentaion: https://docs.docker.com/engine/reference/commandline/build/


Changes: (things that will be updated soon)

- Currently the OSM files, config files, and coordinate files are baked when building the file, in coming updates these files will be added by the user as parameters when running the docker file so that the file is not so large, and customization can be more easily done

