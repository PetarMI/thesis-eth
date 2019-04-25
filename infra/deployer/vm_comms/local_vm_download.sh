#!/bin/bash
#
# Pull Layer 3 IPs from containers and copy them to local

#######################################
# Handle script arguments
#######################################
usage="Script to pull Layer 3 IPs from containers and copy them to local

where:
    -t  The name of the topology to be deployed
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
# Define all constants
#######################################
# VM paths
readonly VM_SCRIPT_DIR="vm_scripts"
readonly VM_NET_STORAGE_DIR="/logs/network"
readonly PULL_SCRIPT="collect_data.sh"

# Local paths
readonly PM_HOME_DIR="$HOME"
readonly PM_WORK_DIR="${PM_HOME_DIR}/thesis-eth/infra/deployer"
readonly PM_IP_DIR="${PM_WORK_DIR}/deployment_files/${FLAG_topology}/net_logs/"

# VM connect info
readonly CONF_FILE="local_vm.conf"
readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Display success or failure of the last executed process
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function check_success {
    local exit_code=$1
    local msg=$2

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}${msg}${NC}\n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

#######################################
# Pull the IP address info from all device containers snd copy it to VM
#######################################
function collect_network_data {
    while IFS=, read -r idx vm_id role
    do
        echo "#### Collecting data on ${role} VM ${idx} ####"
ssh -T "${USER}@${vm_id}" << EOF
    cd ${VM_SCRIPT_DIR}
    ./${PULL_SCRIPT} --${role}
EOF
    done < ${CONF_FILE}
}

#######################################
# Copy IP state info from VMs to local
#######################################
function download_network_data {
    mkdir -p ${PM_IP_DIR}

    while IFS=, read -r idx vm_id role
    do
        echo "#### Downloading from VM ${idx} ####"
        scp "${USER}@${vm_id}:.${VM_NET_STORAGE_DIR}/*" ${PM_IP_DIR} 1>/dev/null
        check_success $? "Downloaded"
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################
echo "###### Collecting Network data on VMs ######"
collect_network_data

echo "###### Downloading Network data ######"
download_network_data
