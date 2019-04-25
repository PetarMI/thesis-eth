## Deployer structure

    ├── composer                # Python scripts for generating compose files
    ├── deployment_files        # Generated files needed for deployment
    │   ├── compose_files       # Composer generated files needed for setting up Docker topology on VM
    │   ├── device_configs      # The updated device_configs (NAT)
    │   ├── nat_files           # Matched addresses and interfaces
    │   ├── net_logs            # Logs downloaded from containers and VMs needed for NAT
    ├── nat                     # Python script for translating subnets, interface names and IP addresses
    └── vm_comms               # dir containing bash scripts that interact with VMs
    
 ## Running
 
 The Deployer does not use any strange python modules but can still be run 
 inside a virtual environment fo convenience. The "odd" dependencies are 
 specified in `requirements.txt`. 
 
 ##### To create an environment:
 1. Create a virtual environment inside a dir of choice
    * `virtualenv venv`
    * `python3 -m venv <venv-name>`
 2. Activate environment inside `/deployer` folder
    * `. <path_to_venv>/venv/bin/activate`
 3. Install required modules
    * `pip install -r requirements.txt`