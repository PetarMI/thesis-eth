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
readonly CONF_FILE="running_vms.conf"
readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

#######################################
# Generic function for calling L2 scripts
#   delegates to L2 to call appropriate L3 script for every container in it
#######################################
function exec_l3_command {
    local option=$1
    pids=()

    while IFS=, read -r idx vm_id role
    do
        printf "${CYAN}#### Running inside VM ${idx} ####${NC}\n"
        ssh -T "${USER}@${vm_id}" "cd ${VM_SCRIPT_DIR}; ./${SETUP_DEVICES} -${option}" &
        pids+=($!)
    done < ${CONF_FILE}

    for pid in ${pids[*]}; do
        wait ${pid}
    done
}

#######################################
# Setup Layer 3 on all VMs
#######################################
function setup_containers {
    exec_l3_command "s"
}

#######################################
# Configure all Layer 3 network devices
#######################################
function configure_devices {
    exec_l3_command "c"
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_setup_devices} == 1 ]]; then
    setup_containers
fi

if [[ ${FLAG_config_devices} == 1 ]]; then
    configure_devices
fi
