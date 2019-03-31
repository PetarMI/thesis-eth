#!/bin/bash
#
# Custom implementation of docker-compose

#######################################
# Handle script arguments
#######################################
usage="Script to setup Layer 2 inside a VM

where:
    --manager  indicates whether the VM is a manager (default: False)
    --help     show this help text"

FLAG_MANAGER=0

while [[ "$1" != "" ]]; do
    case $1 in
        -m | --manager)         FLAG_MANAGER=1
                                ;;
        -w | --worker)          FLAG_MANAGER=0
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        *)                      echo "Unknown flag"
                                exit
                                ;;
    esac
    shift
done

#######################################
# Define all paths
#######################################
readonly COMPOSE_DIR="/home/osboxes/compose/"
readonly NET_FILE="topo_networks.csv"
readonly CONTAINER_FILE="topo_containers.csv"
readonly LINKS_FILE="topo_links.csv"

readonly NET_DRIVER="store/weaveworks/net-plugin:2.5.1"

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

    printf "${msg}..."

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}Success:${NC}\n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}\n"
        exit 1
    fi
}

#######################################
# Create all the network in the topology
#   - This is the first operation to be done
#   - Done on Swarm Manager
#######################################
function create_nets {
    while IFS=, read net_name
    do
        docker network create --driver=${NET_DRIVER} --attachable ${net_name} 1>/dev/null
        check_success $? "Creating network ${net_name}"
    done < ${COMPOSE_DIR}${NET_FILE}
}

#######################################
# Create all the Layer 2 containers destined for that VM
#######################################
function create_containers {
    while IFS=, read -r cont_name net_name image
    do
        docker run -dit --privileged --name=${cont_name} --network=${net_name} ${image} 1>/dev/null
        check_success $? "Creating container ${cont_name}"
    done < ${COMPOSE_DIR}${CONTAINER_FILE}
}

#######################################
# Connect every Layer 2 container to all of its networks
#######################################
function create_links {
    while IFS=, read net_name cont_name
    do
        docker network connect ${net_name} ${cont_name} 1>/dev/null
        check_success $? "Connecting ${cont_name} to network ${net_name}"
    done < ${COMPOSE_DIR}${LINKS_FILE}
}

#######################################
# Whole compose process
#######################################
function compose {
    if [[ ${FLAG_MANAGER} == 1 ]]; then
        echo "## Creating networks on Swarm manager... ##"
        create_nets
    fi

    echo "## Creating containers... ##"
    create_containers

    echo "## Creating links ##"
    create_links
}

if [[ ${FLAG_MANAGER} == 1 ]]; then
        echo "##### Starting setup as MANAGER #####"
    else
        echo "##### Starting setup as WORKER #####"
    fi

compose