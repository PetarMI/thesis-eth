#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script that connects to VMs and does some operation on the containers

where:
    -d     rebuild the Layer 2 image
    -s     setup Layer 3 containers
    -c     configure Layer 3 network devices
    -h     show this help text"

FLAG_build_phynet=0
FLAG_setup_devices=0
FLAG_config_devices=0

while getopts "dsch" option
do
    case "${option}" in
        d) FLAG_build_phynet=1;;
        s) FLAG_setup_devices=1;;
        c) FLAG_config_devices=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Define all constants
#######################################
readonly VM_SCRIPT_DIR="vms-layer1"
readonly SETUP_DEVICES="setup_devices.sh"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

#######################################
# Rebuild the Layer 2 Docker image on every VM
#######################################
function rebuild_docker {
    printf "${RED}Building Layer 2 container not implemented${NC}\n"
}

#######################################
# Setup Layer 3 on all VMs
#   delegated to Layer 2 via script inside each phynet container
#######################################
function setup_layer3 {
    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${SETUP_DEVICES}
EOF
    done < ${CONF_FILE}
}

#######################################
# Configure all Layer 3 network devices
#   delegated to Layer 2 via script inside each phynet container
#######################################
function configure_network_devices {
    printf "${RED}Setting up Layer 3 not implemented${NC}\n"
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_build_phynet} == 1 ]]; then
    echo "##### Rebuilding Layer 2 Docker images #####"
    rebuild_docker
fi

if [[ ${FLAG_setup_devices} == 1 ]]; then
    echo "##### Setting up Layer 3 #####"
    setup_layer3
fi

if [[ ${FLAG_config_devices} == 1 ]]; then
    echo "##### Configuring Layer 3 network devices #####"
    configure_network_devices
fi


