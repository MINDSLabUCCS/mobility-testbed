FROM ubuntu:latest

LABEL maintainer="jason"

ENTRYPOINT ["/bin/bash", "-lc"]

ENV DEBIAN_FRONTEND=noninteractive
ENV APP_PATH=/Users/jason/testbedMultiproc

RUN	apt-get update -y
RUN 	apt-get install tzdata -y --no-install-recommends
RUN	rm -rf /var/lib/apt/lists/*
RUN	ln -fs /usr/share/zoneinfo/America/Denver /etc/localtime \&& dpkg-reconfigure --frontend noninteractive tzdata

RUN	apt-get update -y
RUN	apt-get install vim -y

RUN	apt-get install git cmake python3 g++ libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev python3-dev swig default-jdk maven libeigen3-dev -y
WORKDIR /home
RUN	git clone --recursive https://github.com/eclipse/sumo
RUN	export SUMO_HOME="$PWD/sumo"
RUN	mkdir sumo/build/cmake-build 
WORKDIR /home/sumo/build/cmake-build
RUN	cmake ../..
RUN	ls -lt
RUN	make -j$(nproc)
RUN	make install &&	export SUMO_HOME=/usr/local/share/sumo

RUN	apt-get install python3-venv -y
RUN 	apt-get install osmium-tool -y
RUN	apt-get install sumo-tools -y
RUN	apt-get install gcc -y
RUN	apt-get install g++ -y
RUN	apt-get install proj-bin -y

RUN 	mkdir /home/testbed
RUN 	mkdir /home/testbed/userFiles
RUN 	mkdir /home/testbed/outputMaster

ADD 	ns3 /home/testbed/ns3
ADD 	dockerOutput/userFiles /home/testbed/userFiles
ADD 	src /home/testbed/src

COPY 	requirements.txt /home/testbed/requirements.txt

RUN 	python3 -m venv /home/testbed
WORKDIR /home/testbed
RUN	. ./bin/activate && pip install -r requirements.txt

WORKDIR /
RUN	cd /home/testbed/ns3/ns3-mmwave-antenna && ./waf configure
WORKDIR /home/testbed

CMD	cp /home/testbed/outputMaster/userFiles/config.py /home/testbed/src
