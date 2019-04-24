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
readonly USER="osboxes"
readonly VM_SCRIPT_DIR="vm_scripts"

readonly CONF_FILE="local_vm.conf"
readonly COMPOSE_UP="compose_up.sh"
readonly COMPOSE_DOWN="compose_down.sh"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Auxiliary compose function
# Arguments:
#   script - compose-up or compose-down
#   only_role - execute the script only on VM with this role
#######################################
function compose {
    local script=$1
    local only_role=$2

    while IFS=, read -r idx vm_id role
    do
        if [[ ${only_role} == ${role} ]]
        then
ssh -T "${USER}@${vm_id}" << EOF
    cd ${VM_SCRIPT_DIR}
    ./${script} --${role} --"vm" ${idx}
EOF
        fi
    done < ${CONF_FILE}
}

#######################################
# First compose up the manager where the networks are created
#   and only then create the other containers on worker VMs
#######################################
function compose_up {
    compose "${COMPOSE_UP}" "manager"
    compose "${COMPOSE_UP}" "worker"
}

#######################################
# First remove containers on workers
#   and only then the networks on the manager
#######################################
function compose_down {
    compose "${COMPOSE_DOWN}" "worker"
    compose "${COMPOSE_DOWN}" "manager"
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
