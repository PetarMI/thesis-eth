#!/bin/bash
#
# Executor script which prepares the VMs for fuzzing
# by saving the initial state of the containers right after deployment

#######################################
# Handle script arguments
#######################################
usage="Script to ssh into VM and setup Layer 2

where:
    -d     Deployment state
    -r     Running state
    -h     show this help text"

FLAG_depl=0
FLAG_run=0

while getopts "drh" option
do
    case "${option}" in
        d) FLAG_depl=1;;
        r) FLAG_run=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"

readonly VM_SCRIPT_DIR="fuzz_scripts"
readonly SAVE_DEPL_STATE_SH="save_depl_state.sh"
readonly SAVE_RUN_STATE_SH="save_run_state.sh"

function exec_vm_command {
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

function save_depl_state {
    local command="cd ${VM_SCRIPT_DIR}; ./${SAVE_DEPL_STATE_SH}"
    exec_vm_command "${command}"
}

function save_running_state {
    local command="cd ${VM_SCRIPT_DIR}; ./${SAVE_RUN_STATE_SH}"
    exec_vm_command "${command}"
}

if [[ ${FLAG_run} == 1 ]]; then
    save_running_state
elif [[ ${FLAG_depl} == 1 ]]; then
    save_depl_state
fi
