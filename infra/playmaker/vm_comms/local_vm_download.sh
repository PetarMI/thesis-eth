#!/bin/bash

#######################################
# Define all constants
#######################################
readonly VM_STORAGE_DIR="/home/osboxes/storage"
readonly PM_IP_DIR="/home/pesho/D/thesis-repo/infra/playmaker/nat/network_logs"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

#######################################
# Copy IP state info from VMs to local
#######################################
function download_IPs {
    while IFS=, read -r idx port role
    do
        echo "### Copying interface data from VM ${idx} ###"
        scp -r -P ${port} "${MACHINE}:${VM_STORAGE_DIR}" ${PM_IP_DIR} 1>/dev/null
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

    download_IPs
}