## Backlog 

This document describes the progress and milestones of the network simulator project


### v.0.1.1

##### Release notes

* changes to docker-compose generator 
    * now a class
    * add volumes to Layer 2 containers 
* simple scripts for 
    * pulling and starting an frr container inside Layer 2
    * pushing a config file inside an frr container

##### Project state

* Layer 2 container state
    * volumes: /configs - share the device config files
    * COPY /scripts - for configuring inner FRR 

### v.0.1.0

##### Release notes

* Define json structure that encodes network topology in terms of Layer 2
* python script to produce docker-compose file
    * takes as input the network in json format
    * `docker-compose up` to setup phynet containers and their links
* Write Dockerfile for Layer 2 containers
    * copy FRR Dockerfile and Layer 2 scripts manually into image
* Manually test vtysh commands from Layer 2 to Layer 3

##### Project state

* Layer 2 running on a single host
    * user-defined bridge networks
* Layer 3 (FRR containers) has to be manually setup and configured