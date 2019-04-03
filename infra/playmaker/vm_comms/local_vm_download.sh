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

#######################################
# Define all constants
#######################################
# VM paths
readonly VM_SCRIPT_DIR="vms-layer1"
readonly SETUP_DEVICES="setup_layer3.sh"
readonly VM_STORAGE_DIR="/home/osboxes/storage"

# Local paths
readonly PM_WORK_DIR="/home/pesho/D/thesis-repo/infra/playmaker"
readonly PM_IP_DIR="${PM_WORK_DIR}/nat/network_logs/${FLAG_topology}"

# VM connect info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

#######################################
# Copy IP state info from VMs to local
#######################################
function download_IPs {
    mkdir -p ${PM_IP_DIR}

    while IFS=, read -r idx port role
    do
        echo "### Copying interface data from VM ${idx} ###"
        scp -P ${port} "${MACHINE}:${VM_STORAGE_DIR}/*" ${PM_IP_DIR} 1>/dev/null
    done < ${CONF_FILE}
}

#######################################
# Pull the IP address info from all device containers snd copy it to local
#######################################
function pull_IPs {
    while IFS=, read -r idx port role
    do
        echo "### Running inside VM ${idx}"
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_SCRIPT_DIR}
    ./${SETUP_DEVICES} -i
EOF
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################
echo "##### Pulling IPs #####"
pull_IPs

echo "##### Downloading IPs #####"
download_IPs
