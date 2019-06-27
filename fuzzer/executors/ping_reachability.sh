#!/bin/bash

#######################################
# Script constants
#######################################
readonly WORK_DIR="${HOME}/thesis-eth"
readonly FUZZ_DATA_DIR="${WORK_DIR}/fuzzer/fuzz_data"
readonly INPUT_DATA_DIR="${FUZZ_DATA_DIR}/executor_data"
readonly OUTPUT_DATA_DIR="${FUZZ_DATA_DIR}/verifier_data/ping_logs"

readonly REACH_PROP_FILE="${INPUT_DATA_DIR}/reachability_instr.csv"

readonly PHY_SCRIPT_DIR="/home/api"
readonly PING_SCRIPT="${PHY_SCRIPT_DIR}/reach_ping.sh"

readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly L_GREEN='\033[1;32m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

function prepare_dir {
    rm -rf ${OUTPUT_DATA_DIR}
    mkdir "${OUTPUT_DATA_DIR}"
}

function exec_ping {
    local i=1

    while IFS=, read -r vm_ip cont_name dest_ip
    do
        echo "(${i}) Testing ping reachability from ${cont_name} to ${dest_ip}"
ssh -T "${USER}@${vm_ip}" &> "${OUTPUT_DATA_DIR}/ping_res_${i}.log" << EOF
    docker exec ${cont_name} ${PING_SCRIPT} ${dest_ip}
EOF
        i=$(( $i + 1 ))
    done < ${REACH_PROP_FILE}
}

prepare_dir
exec_ping
