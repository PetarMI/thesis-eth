## Deployer structure

    ├── composer                # Python scripts for generating compose files
    ├── deployment_files        # Generated files needed for deployment
    │   ├── compose_files       # Composer generated files needed for setting up Docker topology on VM
    │   ├── device_configs      # The updated device_configs (NAT)
    │   ├── nat_files           # Matched addresses and interfaces
    │   ├── net_logs            # Logs downloaded from containers and VMs needed for NAT
    ├── nat                     # Python script for translating subnets, interface names and IP addresses
    └── vm_comms               # dir containing bash scripts that interact with VMs

## Running the simulator

1. Have the **Layer 1** VMs up and running 
    * define a `vm.conf` file (vm roles and how to ssh)
    * ensure topology will be setup on a clean directory structure
        * `./vm_env.sh -cd`
2. Setup the **Layer 2** phynet topology
    1. Generate compose files from `.topo`
        * `python TopoComposer.py -t <topo_name>`
    2. Upload all files to VMs (compose, phynet, VM scripts)
        * `./vm_upload.sh -t <topo-name> -a`
        * (if needed) rebuild L2 image `./vm_env.sh -p`
    3. Run compose on VMs
        * `./vm_compose.sh -u`
3. Setup **Layer 3**
    1. Setup the device containers
        * `./vm_configure.sh -s`
    2. Pull network data (IPs) of the Layer 3 containers
        * `./vm_download.sh -t <topo-name>`
    3. Perform NAT
        * `./perform_nat.sh -t <topo-name>`
    4. Upload device configs
        * `./vm_upload.sh -t <topo_name> -f`
    5. Configure Layer 3 devices
        * `./vm_configure.sh -c`