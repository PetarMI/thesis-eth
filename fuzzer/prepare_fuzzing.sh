#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script prepare the data needed for the fuzzing

where:
    -t  The name of the topology being fuzzed
    -h  Show this help text"

FLAG_topology="youforgottopassatopologyname"

while getopts "t:h" option
do
    case "${option}" in
        t) FLAG_topology=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure a topology file has been entered
if [[ ${FLAG_topology} == "youforgottopassatopologyname" ]]; then
        echo "Please topology via -t"
        exit 1
fi

#######################################
# Script constants
#######################################
readonly WORK_DIR="${HOME}/thesis-eth"
readonly FUZZ_DIR="${WORK_DIR}/fuzzer"

readonly FUZZ_DATA_DIR="${FUZZ_DIR}/fuzz_data"
readonly CONTROLLER_DATA_DIR="${FUZZ_DATA_DIR}/controller_data"
readonly EXECUTOR_DATA_DIR="${FUZZ_DATA_DIR}/executor_data"
readonly VERIFIER_DATA_DIR="${FUZZ_DATA_DIR}/verifier_data"

readonly DEPLOY_DIR="${WORK_DIR}/infra/deployer/deployment_files/${FLAG_topology}"
readonly TOPO_DIR="${WORK_DIR}/topologies/${FLAG_topology}"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly L_GREEN='\033[1;32m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color


#######################################
# Only signal if the last executed process failed
#######################################
function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed with exit code ${exit_code}${NC}\n"
        exit ${exit_code}
    fi
}

#######################################
# Collect files related to the currently fuzzed topology
#######################################
function collect_running_data {
    rm -rf "${FUZZ_DATA_DIR}"
    mkdir "${FUZZ_DATA_DIR}"
    mkdir "${CONTROLLER_DATA_DIR}"
    mkdir "${EXECUTOR_DATA_DIR}"
    mkdir "${VERIFIER_DATA_DIR}"

    cp "${TOPO_DIR}/${FLAG_topology}.topo" "${CONTROLLER_DATA_DIR}/topo.json"
    cp "${TOPO_DIR}/properties.json" "${CONTROLLER_DATA_DIR}"
    cp "${DEPLOY_DIR}/nat_files/matched-ips.csv" "${CONTROLLER_DATA_DIR}/nat_ips.csv"
    cp "${WORK_DIR}/infra/deployer/vm_comms/running_vms.conf" "${CONTROLLER_DATA_DIR}"
}

collect_running_data
