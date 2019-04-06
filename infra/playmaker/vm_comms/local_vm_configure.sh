#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script that connects to VMs and does some operation on the containers

where:
    -s     setup Layer 3 containers
    -c     configure Layer 3 network devices
    -h     show this help text"

FLAG_setup_devices=0
FLAG_config_devices=0

while getopts "scih" option
do
    case "${option}" in
        s) FLAG_setup_devices=1;;
        c) FLAG_config_devices=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

#######################################
# Define all constants
#######################################
readonly VM_SCRIPT_DIR="vm_scripts"
readonly SETUP_DEVICES="setup_layer3.sh"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Setup Layer 3 on all VMs
#   delegated to Layer 2 via script inside each phynet container
#######################################
function setup_containers {
    while IFS=, read -r idx port role
    do
        echo "#### Running inside VM ${idx} ####"
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${SETUP_DEVICES} -s
EOF
    done < ${CONF_FILE}
}

#######################################
# Configure all Layer 3 network devices
#   delegated to Layer 2 via script inside each phynet container
#######################################
function configure_devices {
    while IFS=, read -r idx port role
    do
        echo "#### Running inside VM ${idx} ####"
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${SETUP_DEVICES} -c
EOF
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_setup_devices} == 1 ]]; then
    echo "###### Setting up Layer 3 containers ######"
    setup_containers
fi

if [[ ${FLAG_config_devices} == 1 ]]; then
    echo "##### Configuring Layer 3 network devices #####"
    configure_devices
fi
