#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -d     Dropped links
    -r     Restored links
    -s     Strict convergence
    -h     show this help text"

ARG_dropped=""
ARG_restored=""
FLAG_strict=0

while getopts "d:r:sh" option
do
    case "${option}" in
        d) ARG_dropped=${OPTARG};;
        r) ARG_restored=${OPTARG};;
        s) FLAG_strict=1;;
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
readonly RESTORED_CONV_SH="fuzz_conv_restored_strict.sh"

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

# TODO take into account the strict flag
if [[ ${ARG_restored} != "" ]]; then
    printf "${CYAN}## Checking Neighbors convergence${NC}\n"
    time neighbors_convergence

    printf "${CYAN}## Checking Restored links convergence${NC}\n"
    if [[ ${FLAG_strict} == 1 ]]; then
        time restored_convergence
    fi
fi

if [[ ${ARG_dropped} != "" ]]; then
    printf "${CYAN}## Checking Dropped links convergence${NC}\n"
    time dropped_convergence
fi
