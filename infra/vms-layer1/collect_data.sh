#!/bin/bash
#
# Script that pulls and stores data from Layer 2 and Layer 3

#######################################
# Handle script arguments
#######################################
usage="Script to collect network data from Layer 2 and Layer 3

where:
    --manager  indicates that the VM is a manager
    --worker   indicates that the VM is a worker
    --help     show this help text"

FLAG_manager=3

while [[ "$1" != "" ]]; do
    case $1 in
        -m | --manager)         FLAG_manager=1;;
        -w | --worker)          FLAG_manager=0;;
        -h | --help )           echo "$usage"
                                exit;;
        *)                      echo "Unknown flag"
                                exit;;
    esac
    shift
done

# make sure one of containers or networks has been specified
if [[ ${FLAG_manager} == 3 ]]; then
        echo "Please specify whether to run as manager or worker"
        exit 1
fi

#######################################
# Define all constants
#######################################
readonly VM_HOME_DIR="${HOME}"
readonly VM_STORAGE_DIR="${VM_HOME_DIR}/logs"
readonly VM_NET_LOGS_DIR="${VM_STORAGE_DIR}/network"
readonly FRR_INFO_SCRIPT="/home/api/device_info.sh"
readonly NET_LOGS="networks.log"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Display success or failure of the last executed process
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function check_success {
    local exit_code=$1
    local msg=$2

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}${msg}${NC} \n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

#######################################
# Only signal if the last executed process failed
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

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
# Pull and store all IP info from each Layer3 container
#######################################
function pull_device_data {
    check_containers
    mkdir -p ${VM_NET_LOGS_DIR}

    local containers=$(docker ps | grep phynet | awk '{print $NF}')

    while read -r name
    do
        docker exec ${name} ${FRR_INFO_SCRIPT} -i | grep -E '(^Interface|inet)' \
         | awk '{print $2}' > ${VM_NET_LOGS_DIR}/"ipa_${name}.log"
        check_success $? "Saved iface data of container ${name}"
    done <<< ${containers}
}

#######################################
# Save data for all networks that are part of the topology
#   all networks are residing on the Swarm manager
#   so this function should be executed only on the manager
#######################################
function pull_networks_data {
    rm -f ${VM_NET_LOGS_DIR}/${NET_LOGS}
    local networks=$(docker network ls | grep weaveworks | awk '{print $2}')
    local subnet=

    while read -r name
    do
        subnet=$(docker network inspect ${name} | grep Subnet \
        | egrep -o '[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+/[0-9]+')
        signal_fail $? "Extracting subnet data"
        echo "${name},${subnet}" >> ${VM_NET_LOGS_DIR}/${NET_LOGS}
        check_success $? "Saved ${name} subnet data"
    done <<< ${networks}
}

#######################################
# Actual script logic
#   Pulls network data only if running as a Swarm Manager
#######################################
echo "## Pulling Layer 3 device data"
pull_device_data

if [[ ${FLAG_manager} == 1 ]]; then
    echo "## Pulling network data from Swarm Manager ##"
    pull_networks_data
fi
