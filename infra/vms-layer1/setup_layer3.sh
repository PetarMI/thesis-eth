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

while getopts "sch" option
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
readonly HOME="$HOME"
readonly FRR_IMAGE="prefrr.tar"

# L2 constants
readonly SCRIPT_DIR="/home/api"
readonly FRR_SETUP_SCRIPT="${SCRIPT_DIR}/setupFRR.sh"
readonly FRR_CONFIG_SCRIPT="${SCRIPT_DIR}/configFRR.sh"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Report if there are no Layer 2 containers to deploy onto
#######################################
function check_containers {
    local num_containers=$(docker ps | grep -c phynet)

    if [[ ${num_containers} == 0 ]]; then
        printf "${RED}No running containers at $(hostname)${NC}\n"
    fi
}

#######################################
# Send FRR image to every L2 container
#######################################
function setup_frr_image {
    check_containers

    local containers=$(docker ps | grep phynet | awk '{print $NF}')
    pids=()

    echo "## Copying FRR image file to containers... ##"
    while read -r name
    do
        docker cp ${HOME}/${FRR_IMAGE} ${name}:/home/${FRR_IMAGE} &
        pids+=($!)
    done <<< ${containers}

    for pid in ${pids[*]}; do
        wait ${pid}
    done

    printf "${GREEN}Uplaoded image to all containers on VM!${NC}\n"
}

#######################################
# Initiate the Layer3 setup script on all Layer2 containers in parallel
#######################################
function setup_containers {
    local containers=$(docker ps | grep phynet | awk '{print $NF}')
    pids=()

    while read -r name
    do
        echo "## Setting up device on container ${name}... ##"
        # TODO: write to a setup log dir
        docker exec ${name} ${FRR_SETUP_SCRIPT}
    done <<< ${containers}

    printf "${GREEN}Started all L2 containers on VM!${NC}\n"
}

function configure_devices {
    check_containers

    local containers=$(docker ps | grep phynet | awk '{print $NF}')
    pids=()

    while read -r name
    do
        echo "Configuring device on container ${name}..."
        docker exec ${name} ${FRR_CONFIG_SCRIPT} &
        pids+=($!)
    done <<< ${containers}

    for pid in ${pids[*]}; do
        wait ${pid}
    done

    printf "${GREEN}Restarted all L3 cotnainers on VM!${NC}\n"
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_setup_devices} == 1 ]]; then
    time setup_frr_image
    time setup_containers
fi

if [[ ${FLAG_config_devices} == 1 ]]; then
    time configure_devices
fi
