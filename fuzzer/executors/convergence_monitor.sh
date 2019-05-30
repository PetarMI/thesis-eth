#!/bin/bash

readonly USER="fuzzvm"
readonly CONF_FILE="${HOME}/thesis-eth/fuzzer/fuzz_data/controller_data/running_vms.conf"
readonly VM_SCRIPT_DIR="vm_scripts"
readonly CONVERGENCE_SCRIPT="fuzz_convergence.sh"

#function signal_fail {
#    local exit_code=$1
#    local msg=$2
#    if [[ ${exit_code} != 0 ]]; then
#        exit ${exit_code}
#    fi
#}

pids=()

while IFS=, read -r idx vm_id role
do
    ssh -T "${USER}@${vm_id}" "cd ${VM_SCRIPT_DIR}; ./${CONVERGENCE_SCRIPT}" &
    pids+=($!)
done < ${CONF_FILE}

for pid in ${pids[*]}; do
    wait ${pid}
done
