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

FLAG_manager=3
FLAG_vm="undefined"

while [[ "$1" != "" ]]; do
    case $1 in
        -m | --manager)         FLAG_manager=1;;
        -w | --worker)          FLAG_manager=0;;
        -v | --vm)              shift
                                FLAG_vm="$1";;
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

#######################################
# Define all paths
#######################################
readonly HOME_DIR="${HOME}"
readonly COMPOSE_DIR="${HOME_DIR}/compose/"
readonly CONFIG_DIR="${HOME_DIR}/device_configs"
readonly API_DIR="${HOME_DIR}/phynet/api"
readonly NET_FILE="topo_networks.csv"
readonly CONTAINER_FILE="topo_containers.csv"
readonly LINKS_FILE="topo_links.csv"

readonly NET_DRIVER="store/weaveworks/net-plugin:2.5.1"
# readonly NET_DRIVER="weaveworks/net-plugin:latest_release"

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly CYAN='\033[0;36m'
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
        printf "${GREEN}${msg}${NC}\n"
    else
        printf "${RED}Failed with exit code ${exit_code}${NC} ${msg}\n"
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
        check_success $? "Created network ${net_name}"
    done < ${COMPOSE_DIR}${NET_FILE}
}

#######################################
# Create all the Layer 2 containers destined for that VM
#######################################
function create_containers {
    while IFS=, read -r cont_name net_name image
    do
        docker run -dit --privileged --name=${cont_name} --network=${net_name} \
            --hostname=${cont_name} \
            --mount type=bind,source="${CONFIG_DIR}",target=/home/configs \
            --mount type=bind,source="${API_DIR}",target=/home/api \
            ${image} 1>/dev/null
        check_success $? "Created container ${cont_name}"
    done < ${COMPOSE_DIR}${CONTAINER_FILE}
}

#######################################
# Connect every Layer 2 container to all of its networks
#######################################
function create_links {
    while IFS=, read net_name cont_name
    do
        docker network connect ${net_name} ${cont_name} 1>/dev/null
        check_success $? "Connected ${cont_name} to network ${net_name}"
    done < ${COMPOSE_DIR}${LINKS_FILE}
}

#######################################
# Whole compose up process
#######################################
function compose_up {
    if [[ ${FLAG_manager} == 1 ]]; then
        echo "## Creating networks on Swarm manager... ##"
        create_nets
    fi

    echo "## Creating containers... ##"
    create_containers

    echo "## Creating links... ##"
    create_links
}

#######################################
# main()
#######################################
if [[ ${FLAG_manager} == 1 ]]; then
        printf "${CYAN}#### Starting VM ${FLAG_vm} setup as MANAGER ####${NC}\n"
    else
        printf "${CYAN}#### Starting VM ${FLAG_vm} setup as WORKER ####${NC}\n"
fi

compose_up
