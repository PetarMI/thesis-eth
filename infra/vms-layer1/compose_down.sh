#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Compose-down on the VM this is run on

where:
    --manager    compose-down as manager (remove networks)
    --worker     compose-down as worker (only remove containers)
    --vm         which VM it is
    --help       show this help text"

FLAG_manager=3
FLAG_vm="undefined"

while [[ "$1" != "" ]]; do
    case $1 in
        -m | --manager)         FLAG_manager=1;;
        -w | --worker)          FLAG_manager=0;;
        -v | --vm)              shift; FLAG_vm="$1";;
        -h | --help )           echo "$usage"
                                exit;;
        *)                      echo "Unknown flag"
                                exit;;
    esac
    shift
done

# make sure a topology file has been entered
if [[ ${FLAG_manager} == 3 ]]; then
        echo "Please specify role using --manager or --worker"
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
# Whole compose_down process
#######################################
function compose_down {
    echo "## Stopping containers ##"
    stop_containers

    echo "## Removing containers ##"
    rm_containers

    if [[ ${FLAG_manager} == 1 ]]
    then
        echo "## Removing networks ##"
        rm_networks
    fi
}

#######################################
# main()
#######################################
if [[ ${FLAG_manager} == 1 ]]; then
        echo "#### Starting VM ${FLAG_vm} teardown as MANAGER ####"
    else
        echo "#### Starting VM ${FLAG_vm} teardown as WORKER ####"
fi

compose_down
