#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -d     Dropped links
    -r     Restored links
    -h     show this help text"

ARG_dropped=""
ARG_restored=""

while getopts "d:r:h" option
do
    case "${option}" in
        d) ARG_dropped=${OPTARG};;
        r) ARG_restored=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"

# convergence checking scripts at the VMs
readonly VM_SCRIPT_DIR="vm_scripts"
readonly DROPPED_CONV_SH="fuzz_conv_dropped.sh"
readonly NEIGHBORS_CONV_SH="fuzz_conv_neighbors.sh"
readonly RESTORED_CONV_SH="fuzz_conv_restored.sh"

readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

function vm_convergence {
    local command="$1"

    local pids=()

    while IFS=, read -r idx vm_id role
    do
        ssh -T "${USER}@${vm_id}" "${command}" &
        pids+=($!)
    done < ${CONF_FILE}

    for pid in ${pids[*]}; do
        wait ${pid}
    done
}


function dropped_convergence {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${DROPPED_CONV_SH} ${ARG_dropped}"
    vm_convergence "${cmd}"
}

function neighbors_convergence {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_CONV_SH}"
    vm_convergence "${cmd}"
}

function restored_convergence {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${RESTORED_CONV_SH} ${ARG_restored}"
    vm_convergence "${cmd}"
}


printf "${CYAN}## Checking Dropped links convergence${NC}\n"
time dropped_convergence

printf "${CYAN}## Checking Neighbors convergence${NC}\n"
time neighbors_convergence

#printf "${CYAN}## Checking Restored links convergence${NC}\n"
#time restored_convergence
