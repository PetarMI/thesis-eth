## Network Simulator

Directory containing all infrastructure logic.

### Playmaker

Includes all the logic for setting up the topology

* VM interactions

### Layer 1 - VMs

Infrastructure Layer 1 consists of Virtual Machines which host several Layer 2 container.

##### Requirements 

* Network connectivity between all machines 
* Running Docker

##### VM types

* Local VMs (`VirtualBox`)
    * managed through `docker-compose` (handles a lot of functionality)
    * `docker-compose` also supports Azure, AWS, etc.
* Independent cloud VMs (ex. ETH machines)
    * managed through ssh


### Layer 2 - Phynet 

Logic inside the Phynet containers 

* setting up FRR containers
* configuring FRR containers 
* changing FRR configs via `vtysh` commands