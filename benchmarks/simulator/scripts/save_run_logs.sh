#!/bin/bash

ARG_topo="$1"
ARG_run="$2"

# VM paths
readonly VM_LOG="/logs/setup.log"

# Local paths
readonly HOME_DIR="$HOME"
readonly BENCH_DIR="${HOME_DIR}/thesis-eth/benchmarks/simulator/depl_files"
readonly RUN_DIR="${BENCH_DIR}/${ARG_topo}/run_${ARG_run}"
readonly LAST_RUN_LOG="${BENCH_DIR}/latest_run/depl_stats.log"

# VM connect info
readonly CONF_FILE="${HOME}/thesis-eth/infra/deployer/vm_comms/running_vms.conf"
readonly USER="fuzzvm"

function check_existing_logs {
    if [ "$(ls -A $RUN_DIR)" ]; then
        echo "${RUN_DIR} is not Empty"
        exit 1
    fi
}

function move_overview_data {
    echo "Moving high-level data from deploy.sh"
    cp "${LAST_RUN_LOG}" "${RUN_DIR}"
}

function download_setup_logs {
    echo "#### Downloading setup logs from VMs ####"

    while IFS=, read -r idx vm_id role
    do
        echo "Downloading from VM ${idx}"
        scp "${USER}@${vm_id}:.${VM_LOG}" "${RUN_DIR}/setup_${idx}.log" 1>/dev/null
    done < ${CONF_FILE}
}

function clear_last_run {
    > "${LAST_RUN_LOG}"
}

mkdir -p ${RUN_DIR}
check_existing_logs
move_overview_data
download_setup_logs
clear_last_run

