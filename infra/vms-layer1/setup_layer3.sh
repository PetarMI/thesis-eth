#!/bin/bash

# TODO: This script works only with FRR containers for now

#######################################
# Handle script arguments
#######################################
usage="Script that sets up and configs the network device container on top of
every Layer 2 container residing on that VM

where:
    -s     setup Layer 3 containers
    -c     configure Layer 3 network devices
    -h     show this help text"

FLAG_setup_devices=0
FLAG_config_devices=0
FLAG_pull_IPs=0

while getopts "scih" option
do
    case "${option}" in
        s) FLAG_setup_devices=1;;
        c) FLAG_config_devices=1;;
        i) FLAG_pull_IPs=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

#######################################
# Define all constants
#######################################
#VM paths
readonly VM_STORAGE_DIR="/home/osboxes/storage"

# Layer 3 scripts
readonly FRR_SETUP_SCRIPT=/home/scripts/setupFRR.sh
readonly FRR_IP_SCRIPT="/home/api/get_ips.sh"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Report if there are no Layer 3 containers to deploy onto
#######################################
function check_containers {
    local num_containers=$(docker ps | grep -c phynet)

    if [[ ${num_containers} == 0 ]]; then
        printf "${RED}No running containers at $(hostname)${NC}\n"
    fi
}

#######################################
# Initiate the setup script on all Layer 2 containers in parallel
#######################################
function setup_containers {
    check_containers

    local containers=$(docker ps | grep phynet | awk '{print $NF}')
    pids=()

    while read -r name
    do
        echo "Setting up device on container ${name}..."
        docker exec ${name} ${FRR_SETUP_SCRIPT} 1 >/dev/null &
        pids+=($!)
    done <<< ${containers}

    echo "Processing..."

    # wait for all containers to finish setting up
    for pid in ${pids[*]}; do
        wait ${pid}
    done

    printf "${GREEN}### Done! ${NC}\n"
}

function pull_IPs {
    check_containers

    local containers=$(docker ps | grep phynet | awk '{print $NF}')

    while read -r name
    do
        echo "Saving network data of container ${name}..."
        docker exec ${name} ${FRR_IP_SCRIPT} > ${VM_STORAGE_DIR}/"ips_${name}.log"
    done <<< ${containers}
}

function configure_devices {
    printf "${RED}Device configs not implemented on VMs${NC}\n"
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_setup_devices} == 1 ]]; then
    setup_containers
fi

if [[ ${FLAG_pull_IPs} == 1 ]]; then
    pull_IPs
fi

if [[ ${FLAG_config_devices} == 1 ]]; then
    configure_devices
fi
