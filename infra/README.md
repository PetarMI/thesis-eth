# Network Simulator

## Running the simulator

1. Have the **Layer 1** VMs up and running 
    * define a `vm.conf` file (vm roles and how to ssh)
    * ensure topology will be setup on a clean directory structure
        * `./local_vm_env.sh -cd`
2. Setup the **Layer 2** phynet topology
    1. Generate compose files from `.topo`
        * `python TopoComposer.py -t <topo_name>`
    2. Upload all files to VMs (compose, phynet, VM scripts)
        * `./local_vm_upload.sh -t <topo-name> -a`
        * (if needed) rebuild L2 image `./local_vm_env.sh -p`
    3. Run compose on VMs
        * `./local_vm_compose.sh -u`
3. Setup **Layer 3**
    1. Setup the device containers
        * `./local_vm_configure.sh -s`
    2. Pull network data (IPs) of the Layer 3 containers
        * `./local_vm_download.sh -t <topo-name>`
    3. Perform NAT
        * `./perform_nat.sh -t <topo-name>`
    4. Upload device configs
        * `./local_vm_upload.sh -t <topo_name> -f`
    5. Configure Layer 3 devices
        * `./local_vm_configure.sh -c`

## Architecture

Directory containing all infrastructure logic.

### Deployer

Includes all the logic for setting up the topology

* Generate compose files
* VM interactions (upload files, init compose, download Layer 2 network info)
* Performing NAT

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