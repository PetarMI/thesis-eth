## pre-Releases 

This document describes the progress of manually setting up the infrastructure of the 
network simulator. 

The versions described here do not contain code or github commits but rather refer to 
setting up, configuring and generally trying virtual machines, containers, networks, 
etc.


#### v.0.0.4 - FRR setup via vtysh commands

Configure FRR using vtysh shell commands. To be used later in scripts.

#### v.0.0.3 - Layer 3 using Docker and FRR

##### Release notes 

* Docker containers running Debian
    * Docker is running frr as its main process
* Dockerfile that installs FRR via packages
* Dockers connected via custom bridge networks
* FRR configured via a global frr.conf file


#### v.0.0.2 - Layer 3 using VMs and FRR

##### Release notes

* VMs running Ubuntu Server 18.04
* internal network connections between VMs
* install FRR via packages
* configure OSPF via frr.conf 

#### v.0.0.1 - Docker containers in an overlay network

Use an overlay network to enable two containers residing on separate Docker hosts
to communicate.

##### Setup

* Docker hosts are Docker enabled local VMs
    * NAT and Host-only adapter


