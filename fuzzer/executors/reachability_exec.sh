#!/bin/bash

#######################################
# Script constants
#######################################
readonly WORK_DIR="${HOME}/thesis-eth"
readonly FUZZ_DIR="${WORK_DIR}/fuzzer"
readonly FUZZ_DATA_DIR="${FUZZ_DIR}/fuzz_data"
readonly REACH_FILE="${FUZZ_DATA_DIR}/reachability_props.csv"

readonly PHY_SCRIPT_DIR="/home/api"
readonly PING_SCRIPT="${PHY_SCRIPT_DIR}/reach_ping.sh"

readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly L_GREEN='\033[1;32m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

function exec_ping {
    while IFS=, read -r vm_ip cont_name dest_ip
    do
        printf "${CYAN}#### Testing reachability from ${cont_name} to ${dest_ip} ####${NC}\n"
ssh -T "${USER}@${vm_ip}" << EOF
    docker exec ${cont_name} ${PING_SCRIPT} ${dest_ip}
EOF
    done < ${REACH_FILE}
}

exec_ping
