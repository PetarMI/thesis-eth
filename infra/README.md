# Network Simulator

## Deployer structure

    ├── composer                # Python scripts for generating compose files
    ├── deployment_files        # Generated files needed for deployment
    │   ├── compose_files       # Composer generated files needed for setting up Docker topology on VM
    │   ├── device_configs      # The updated device_configs (NAT)
    │   ├── nat_files           # Matched addresses and interfaces
    │   ├── net_logs            # Logs downloaded from containers and VMs needed for NAT
    ├── nat                     # Python script for translating subnets, interface names and IP addresses
    └── vm_comms      

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
* ssh to VMs 
* Running Docker
* `weavenet` driver
* `rp_filter` set to 2

### Layer 2 - Phynet 

Logic inside the Phynet containers 

* setting up FRR containers
* configuring FRR containers 
* changing FRR configs via `vtysh` commands