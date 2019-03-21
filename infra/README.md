## Network Simulator

Directory containing all infrastructure logic.

### Layer 1

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
