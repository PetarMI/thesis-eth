#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Compose-down on the VM this is run on

where:
    -c     stop and remove containers
    -n     remove networks
    -h     show this help text"

FLAG_containers=0
FLAG_networks=0

while getopts "cnh" option
do
    case "${option}" in
        c) FLAG_containers=1;;
        n) FLAG_networks=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure one of containers or networks has been specified
if [[ ${FLAG_containers} == 0 ]] && [[ ${FLAG_networks} == 0 ]]; then
        echo "Please specify containers (-c) or networks (-n)"
        exit 1
fi

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Stop all containers on VM
#######################################
function stop_containers {
    local running_containers=$(docker ps | grep -c Up)

    if [[ ${running_containers} == 0 ]]; then
        printf "${GREEN}No running containers at $(hostname)${NC}\n"
    else
        docker ps | grep Up | awk '{print $NF}' | xargs -n1 docker container stop
    fi
}

#######################################
# Remove all containers on VM
#######################################
function rm_containers {
    stopped_containers=$(docker ps -a | grep -c Exited)

    if [[ ${stopped_containers} == 0 ]]; then
        printf "${GREEN}No stopped containers at $(hostname)${NC}\n"
    else
        docker ps -a | grep Exited | awk '{print $NF}' | xargs -n1 docker container rm
    fi
}

#######################################
# Remove all networks on the VM
#   will rmeove stuff only on the Swarm manager
#######################################
function rm_networks {
    num_nets=$(docker network ls | grep -c weaveworks)

    if [[ ${num_nets} == 0 ]]; then
        printf "${GREEN}No networks at $(hostname)${NC}\n"
    else
        docker network ls | grep weaveworks | awk '{print $2}' | xargs -n1 docker network rm
    fi
}


#######################################
# Actual script logic
#   Remove either container or networks
#######################################

if [[ ${FLAG_containers} == 1 ]]
then
    echo "## Stopping containers ##"
    stop_containers

    echo "## Removing containers ##"
    rm_containers
elif [[ ${FLAG_networks} == 1 ]]
then
    echo "## Removing networks ##"
    rm_networks
fi
