# Network Simulator

## Running the simulator

1. Have the **Layer 1** VMs up and running 
    * define a `vm.conf` file (manager and how to ssh)
2. Setup the **Layer 2** phynet topology
    1. Generate compose files from `.topo`
        * `python TopoComposer.py -f <path-to-topo-file>`
    2. Upload all files to VMs
        * `./local_vm_upload.sh -t <topo-name> -a`
        * compose files, phynet files (Docker + scripts) and VM scripts
    3. Run compose on VMs
        * `./local_vm_compose.sh -u`
3. Setup **Layer 3**
    1. Setup the device containers
        * `./local_vm_configure.sh -s`

## Architecture

Directory containing all infrastructure logic.

### Playmaker

Includes all the logic for setting up the topology

* Generate compose files
* VM interactions (upload files, init compose)

### Layer 1 - VMs

Infrastructure Layer 1 consists of Virtual Machines which host several Layer 2 container.

##### Requirements 

* Network connectivity between all machines 
* Running Docker
* `weavenet` driver

##### VM types

* Local VMs (`VirtualBox`)
* Independent cloud VMs (ex. ETH machines)
    * managed through ssh

### Layer 2 - Phynet 

Logic inside the Phynet containers 

* setting up FRR containers
* configuring FRR containers 
* changing FRR configs via `vtysh` commands