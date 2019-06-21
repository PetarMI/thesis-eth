#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -d     Dropped links
    -f     Full revert links
    -p     Partial revert links
    -h     show this help text"

ARG_dropped=""
ARG_full_revert=""
ARG_partial_revert=""

while getopts "d:f:p:h" option
do
    case "${option}" in
        d) ARG_dropped=${OPTARG};;
        f) ARG_full_revert=${OPTARG};;
        p) ARG_partial_revert=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"

# convergence checking scripts at the VMs
readonly VM_SCRIPT_DIR="fuzz_scripts"
readonly DROPPED_CONV_SH="conv_dropped.sh"
readonly RESTORE_CONV_FULL_SH="conv_restored_full.sh"
readonly NEIGHBORS_UP_FULL_SH="neighbors_up_full.sh"
readonly NEIGHBORS_UP_PARTIAL_SH="neighbors_up_partial.sh"
readonly NEIGHBORS_ADJ_SH="neighbor_adj.sh"
readonly ROUTES_UP_FULL_SH="routes_up_full.sh"
readonly ROUTES_UP_PARTIAL_SH="routes_up_partial.sh"
readonly ROUTE_CHANGES_SH="route_changes.sh"

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

function revert_convergence_full {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${RESTORE_CONV_FULL_SH} ${ARG_full_revert}"
    vm_convergence "${cmd}"
}

function neighbors_up_full {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_UP_FULL_SH}"
    vm_convergence "${cmd}"
}

function neighbors_up_partial {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_UP_PARTIAL_SH} ${ARG_partial_revert}"
    vm_convergence "${cmd}"
}

function neighbors_adjacency {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${NEIGHBORS_ADJ_SH}"
    vm_convergence "${cmd}"
}

function routes_up_full {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${ROUTES_UP_FULL_SH}"
    vm_convergence "${cmd}"
}

function routes_up_partial {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${ROUTES_UP_PARTIAL_SH}"
    vm_convergence "${cmd}"
}

function route_changes {
    local cmd="cd ${VM_SCRIPT_DIR}; ./${ROUTE_CHANGES_SH}"
    vm_convergence "${cmd}"
}


if [[ ${ARG_dropped} != "" ]]; then
    printf "${CYAN}## Checking Dropped links convergence${NC}\n"
    time dropped_convergence

elif [[ ${ARG_partial_revert} != "" ]]; then
    printf "${CYAN}## Checking Neighbors adjacency${NC}\n"
    time neighbors_up_partial
    time neighbors_adjacency

    printf "${CYAN}## Checking Routes changes${NC}\n"
    time route_changes

elif [[ ${ARG_full_revert} != "" ]]; then
    printf "${CYAN}## Checking Neighbors adjacency${NC}\n"
    time neighbors_up_full
    time neighbors_adjacency

    printf "${CYAN}## Checking Restored links convergence${NC}\n"
    time revert_convergence_full

    printf "${CYAN}## Checking Routes restore${NC}\n"
    time routes_up_full
fi
