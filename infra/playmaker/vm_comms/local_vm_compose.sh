#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -u     compose UP
    -d     compose DOWN
    -h     show this help text"

FLAG_UP=3

while getopts "udh" option
do
    case "${option}" in
        u) FLAG_UP=1;;
        d) FLAG_UP=0;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure a topology file has been entered
if [[ ${FLAG_UP} == 3 ]]; then
        echo "Please specify up (-u) or down (-d)"
        exit 1
fi

#######################################
# Define paths and constants
#######################################
readonly MACHINE="osboxes@localhost"
readonly VM_WORK_DIR="/home/osboxes"
readonly VM_SCRIPT_DIR="vms-layer1"

readonly CONF_FILE="local_vm.conf"
readonly COMPOSE_UP="compose_up.sh"
readonly COMPOSE_DOWN="compose_down.sh"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Initiate compose -up script on all VMs
#######################################
function compose_up {
    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${COMPOSE_UP} --${role}
EOF
    done < ${CONF_FILE}
}

#######################################
# The main compose-down function
#   First remove all containers and only then the networks
#   otherwise it will fail at the networks as there will be attached containers
#######################################
function compose_down {
    compose_down_aux "c"
    compose_down_aux "n"
}

#######################################
# Deletes either container or networks
#######################################
function compose_down_aux {
    local what_to_remove=$1

    while IFS=, read -r idx port role
    do
        echo "#### Working on VM ${idx} ####"
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${COMPOSE_DOWN} -${what_to_remove}
EOF
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################

if [[ ${FLAG_UP} == 1 ]]
then
    echo "###### Compose UP ######"
    compose_up
elif [[ ${FLAG_UP} == 0 ]]
then
    echo "###### Compose DOWN ######"
    compose_down
fi
