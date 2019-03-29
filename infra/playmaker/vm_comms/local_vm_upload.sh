#!/bin/bash
#
# Copy all necessary files into the VMs

#######################################
# Handle script arguments
#######################################
usage="Script to upload all needed files on the VMs

where:
    -t  The name of the topology to be deployed
    -a  Upload all files
    -c  Upload compose files
    -d  Upload docker files
    -h  Show this help text"

topology="botevvratsa"
compose_files=0
docker_files=0

while getopts "t:acdh" option
do
    case "${option}" in
        t) topology=${OPTARG};;
        a) compose_files=1;
           docker_files=1;;
        c) compose_files=1;;
        d) docker_files=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure a topology file has been entered
if [[ ${topology} == "botevvratsa" ]]; then
        echo "No topology argument provided via -f flag"
        exit 1
fi

#######################################
# Define all paths
#######################################
# VM paths
readonly VM_WORK_DIR="/home/osboxes"
readonly VM_COMPOSE_DIR="${VM_WORK_DIR}/compose"
readonly VM_DOCKER_DIR="${VM_WORK_DIR}/phynet"
readonly VM_SCRIPT_DIR="${VM_WORK_DIR}/scripts"

readonly VM_NET_FILE="${VM_COMPOSE_DIR}/topo_networks.csv"
readonly VM_CONTAINERS_FILE="${VM_COMPOSE_DIR}/topo_containers.csv"
readonly VM_LINKS_FILE="${VM_COMPOSE_DIR}/topo_links.csv"

# paths on localhost
readonly PM_WORK_DIR="/home/pesho/D/thesis-repo/infra"
readonly PM_COMPOSE_DIR="${PM_WORK_DIR}/playmaker/build_instr/${topology}"
readonly PM_DOCKER_DIR="${PM_WORK_DIR}/phynet-layer2"
readonly PM_SCRIPT_DIR="${PM_WORK_DIR}/vms-layer1"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

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

    printf "${msg}..."

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}Success${NC}\n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}\n"
        exit ${exit_code}
    fi
}

#######################################
# Only signal if the last executed process failed
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

function setup_dir_structure {
    echo "TODO - Ensure VM has all necessary folders to copy into"

    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    rm -r compose/*
EOF
    done < ${CONF_FILE}
}

#######################################
# Upload all files necessary to do a compose up on the VM
#   - networks at the Swarm manager
#   - containers to be started at each VM
#   - links for every container
#######################################
function upload_compose_files {
    while IFS=, read -r idx port role #|| [ -n "${cont_name}" ]
    do
        local src_nets="${PM_COMPOSE_DIR}/net-compose.csv"
        scp -P ${port} ${src_nets} "${MACHINE}:${VM_NET_FILE}"
        signal_fail $? "Copying networks file"

        local src_conts="${PM_COMPOSE_DIR}/netvm${idx}_containers.csv"
        scp -P ${port} ${src_conts} "${MACHINE}:${VM_CONTAINERS_FILE}"
        signal_fail $? "Copying containers file"

        local src_links="${PM_COMPOSE_DIR}/netvm${idx}_links.csv"
        scp -P ${port} ${src_links} "${MACHINE}:${VM_LINKS_FILE}"
        signal_fail $? "Copying links file"
    done < ${CONF_FILE}
}

#######################################
# Upload all Layer 2 related files
#   - Phynet image Dockerfile
#   - Scripts residing in each Layer 2 container (API)
#######################################
function update_docker_files {
    while IFS=, read -r idx port role
    do
        local src_scripts="${PM_DOCKER_DIR}/scripts"
        scp -r -P ${port} ${src_scripts} "${MACHINE}:${VM_DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet scripts to VM ${idx}"

        local src_docker="${PM_DOCKER_DIR}/Dockerfile"
        scp -P ${port} ${src_docker} "${MACHINE}:${VM_DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet Dockerfile to VM ${idx}"
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################

if [[ ${compose_files} == 1 ]]; then
        echo "### Sending compose files to VMs ###"
fi

if [[ ${docker_files} == 1 ]]; then
        echo "### Sending phynet files to VMs ###"
fi

#echo "### Setting up directory structure on VMs ###"
#setup_dir_structure

#echo "### Sending phynet files to VMs ###"
# update_docker_files

#echo "### Sending compose files to VMs ###"
#upload_compose_files
# echo "${INPUT_DIR}"