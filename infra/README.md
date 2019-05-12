# Network Simulator

## Running the simulator

```bash
./deploy.sh -t <topo-name>
```

### Deployer

Includes all the logic for setting up the topology

* Generate compose files
* VM interactions (upload files, init compose, download Layer 2 network info)
* Performing NAT

### Layer 1 - VMs

Infrastructure Layer 1 consists of Virtual Machines which host several Layer 2 container.

##### Requirements 

* Network connectivity between all machines 
    * internal network used by Docker swarm
* ssh to VMs (ex. `virbr0`/`vboxnet0`)
* Running Docker
* `weavenet` driver
* `rp_filter` set to 2

### Layer 2 - Phynet 

Logic inside the Phynet containers 

* setting up FRR containers
* configuring FRR containers 
* changing FRR configs via `vtysh` commands