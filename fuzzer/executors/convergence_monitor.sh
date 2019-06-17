#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -d     Dropped links
    -f     Full revert links
    -h     show this help text"

ARG_dropped=""
ARG_full_revert=""

while getopts "d:f:h" option
do
    case "${option}" in
        d) ARG_dropped=${OPTARG};;
        f) ARG_full_revert=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"

# convergence checking scripts at the VMs
readonly VM_SCRIPT_DIR="vm_scripts"
readonly DROPPED_CONV_SH="fuzz_conv_dropped.sh"
readonly NEIGHBORS_UP_SH="fuzz_neighbors_up.sh"
readonly NEIGHBORS_ADJ_SH="fuzz_neighbor_adj.sh"
readonly FULL_RESTORE_CONV_SH="fuzz_conv_restored_full.sh"
readonly ROUTES_UP_SH="fuzz_routes_up.sh"

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

function neighbors_up {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_UP_SH}"
    vm_convergence "${cmd}"
}

function neighbors_adjacency {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_ADJ_SH}"
    vm_convergence "${cmd}"
}

function full_revert_convergence {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${FULL_RESTORE_CONV_SH} ${ARG_full_revert}"
    vm_convergence "${cmd}"
}

function routes_up {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${ROUTES_UP_SH}"
    vm_convergence "${cmd}"
}

function dropped_convergence {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${DROPPED_CONV_SH} ${ARG_dropped}"
    vm_convergence "${cmd}"
}


if [[ ${ARG_full_revert} != "" ]]; then
    printf "${CYAN}## Checking Neighbors adjacency${NC}\n"
    time neighbors_up
    time neighbors_adjacency

    printf "${CYAN}## Checking Restored links convergence${NC}\n"
    time full_revert_convergence

    printf "${CYAN}## Checking Routes restore${NC}\n"
    time routes_up
fi

if [[ ${ARG_dropped} != "" ]]; then
    printf "${CYAN}## Checking Dropped links convergence${NC}\n"
    time dropped_convergence
fi
