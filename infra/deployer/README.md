## Deployer structure

    ├── composer                # Python scripts for generating compose files
    ├── deployment_files        # Generated files needed for deployment
    │   ├── compose_files       # Composer generated files needed for setting up Docker topology on VM
    │   ├── device_configs      # The updated device_configs (NAT)
    │   ├── nat_files           # Matched addresses and interfaces
    │   ├── net_logs            # Logs downloaded from containers and VMs needed for NAT
    ├── nat                     # Python script for translating subnets, interface names and IP addresses
    └── vm_comms               # dir containing bash scripts that interact with VMs
    