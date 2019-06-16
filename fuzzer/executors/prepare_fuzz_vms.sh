#!/bin/bash
#
# Executor script which prepares the VMs for fuzzing

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"

readonly VM_SCRIPT_DIR="vm_scripts"
readonly LOG_NEIGHBORS_SH="log_neighbors.sh"

function vm_prepare {
    local command="cd ${VM_SCRIPT_DIR}; ./${LOG_NEIGHBORS_SH}"

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

vm_prepare
