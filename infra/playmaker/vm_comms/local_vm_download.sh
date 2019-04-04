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
readonly VM_SCRIPT_DIR="vms-layer1"
readonly PULL_SCRIPT="collect_data.sh"
readonly VM_STORAGE_DIR="/home/osboxes/storage"

# Local paths
readonly PM_WORK_DIR="/home/pesho/D/thesis-repo/infra/playmaker"
readonly PM_IP_DIR="${PM_WORK_DIR}/deployment_files/${FLAG_topology}/net_logs/"

# VM connect info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

#######################################
# Pull the IP address info from all device containers snd copy it to local
#######################################
function pull_network_data {
    while IFS=, read -r idx port role
    do
        echo "#### Pulling data from VM ${idx}"
ssh -T -p ${port} ${MACHINE} << EOF
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

    while IFS=, read -r idx port role
    do
        echo "#### Copying interface data from VM ${idx} ####"
        scp -P ${port} "${MACHINE}:${VM_STORAGE_DIR}/*" ${PM_IP_DIR} 1>/dev/null
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################
echo "###### Pulling Network data ######"
pull_network_data

echo "###### Downloading Network data ######"
download_network_data
