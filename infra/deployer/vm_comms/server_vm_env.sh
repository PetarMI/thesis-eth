#!/bin/bash
#
# Script for setting up and checking the server VMs

#######################################
# Handle script arguments
#######################################
usage="Script for setting up and checking the server VMs

where:
    -s     start VMs
    -z     stop VMs
    -v     verify running VM stuff
    -h     show this help text"

FLAG_start=0
FLAG_stop=0
FLAG_image=0s
FLAG_verify=0

while getopts "s:zvih" option
do
    case "${option}" in
        s) FLAG_start=${OPTARG}
           FLAG_stop=0;;
        z) FLAG_start=0
           FLAG_stop=1;;
        v) FLAG_verify=1;;
        i) FLAG_image=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly VM_NAME="fuzzvm"
readonly CONF_FILE="running_vms.conf"
readonly FRR_IMAGE="prefrr.tar"

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

running_vms=()
function get_running_vms {
    while IFS= read -r rvm; do
        running_vms+=( "${rvm}" )
    done < <( virsh list | grep running | awk '{print $2}' )
}

function startVMs {
    for i in $(seq 0 $(( ${FLAG_start} - 1 ))); do
        virsh start "${VM_NAME}${i}" 1>/dev/null
        check_success $? "Started ${VM_NAME}${i}"
    done
}

function stopVMs {
    for rvm in "${running_vms[@]}"; do
        virsh shutdown "${rvm}" 1>/dev/null
        check_success $? "Stopped ${rvm}"
    done < <( virsh list | grep running | awk '{print $2}' )
}

function setupSSHAgent {
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa_fuzzvm
    check_success $? "SSH key added"
}

function upload_FRR_img {
    while IFS=, read -r idx vm_id role
    do
        echo "Sending image to VM ${idx}"
        scp "${HOME}/${FRR_IMAGE}" ${VM_NAME}@${vm_id}:./
        check_success $? "Success"
    done < ${CONF_FILE}
}

function verifyIPs {
    echo "Follow the tutorial"
}

function checkSwarm {
    echo "Not implemented"
}

#######################################
# Actual script logic
#######################################
if [[ ${FLAG_start} -gt 0 ]]; then
    echo "##### Starting VMs #####"
    startVMs

    echo "##### Adding ssh keys to agent #####"
    setupSSHAgent
fi

if [[ ${FLAG_image} == 1 ]]; then
    echo "##### Sending FRR image #####"
    upload_FRR_img
fi

if [[ ${FLAG_verify} == 1 ]]; then
    echo "##### Verifying virbr0 IPs #####"
    verifyIPs

    echo "##### Checking swarm #####"

fi

if [[ ${FLAG_stop} == 1 ]]; then
    echo "##### Stopping VMs #####"
    get_running_vms
    stopVMs
fi

