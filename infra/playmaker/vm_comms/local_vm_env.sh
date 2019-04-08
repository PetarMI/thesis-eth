#!/bin/bash
#
# Script containing functions that check and setup the VM environment

#######################################
# Handle script arguments
#######################################
usage="Script for checking and setting up the VM environment

where:
    -c     clean VM dirs
    -d     setup dir structure
    -p     rebuild the Layer 2 image
    -v     view Dir structure
    -h     show this help text"

FLAG_clean=0
FLAG_dirs=0
FLAG_build_phynet=0
FLAG_view=0

while getopts "cdovh" option
do
    case "${option}" in
        c) FLAG_clean=1;;
        d) FLAG_dirs=1;;
        p) FLAG_build_phynet=1;;
        v) FLAG_view=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

#######################################
# Define all paths
#######################################
# VM paths
readonly VM_WORK_DIR="/home/osboxes"
readonly VM_COMPOSE_DIR="compose"
readonly VM_DOCKER_DIR="phynet"
readonly VM_SCRIPT_DIR="vm_scripts"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

function clean {
    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_WORK_DIR}
    rm -rf *
EOF
    done < ${CONF_FILE}
}

function setup_dir_structure {
    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    cd ${VM_WORK_DIR}
    mkdir -p ${VM_COMPOSE_DIR}
    mkdir -p ${VM_DOCKER_DIR}
    mkdir -p ${VM_SCRIPT_DIR}
EOF
    done < ${CONF_FILE}

    echo "## Created directories:"
    printf "${GREEN}/${VM_COMPOSE_DIR}${NC} - store compose files for the particular VM\n"
    printf "${GREEN}/${VM_DOCKER_DIR}${NC} - store Layer 2 Dockerfile and scripts\n"
    printf "${GREEN}/${VM_SCRIPT_DIR}${NC} - store Layer 1 scripts\n"
    echo "## Dirs created during upload"
    printf "${GREEN}/phynet/scripts${NC} - store the Layer 2 scripts\n"
    printf "${GREEN}/device_configs${NC} - store config files for all topology devices\n"
}

function view {
    while IFS=, read -r idx port role
    do
        if [[ ${role} == "manager" ]]
        then
ssh -T -p ${port} ${MACHINE} << EOF
    ls -lR
EOF
            break
        fi
    done < ${CONF_FILE}
}

#######################################
# Rebuild the Layer 2 Docker image on every VM
#######################################
function rebuild_docker {
    printf "${RED}Building Layer 2 container not implemented${NC}\n"
}

if [[ ${FLAG_clean} == 1 ]]; then
    echo "##### Cleaning VM directories #####"
    clean
fi

if [[ ${FLAG_dirs} == 1 ]]; then
    echo "##### Building VM dir structure #####"
    setup_dir_structure
fi

if [[ ${FLAG_view} == 1 ]]; then
    echo "##### View VM dir structure #####"
    view
fi

if [[ ${FLAG_build_phynet} == 1 ]]; then
    echo "##### Rebuilding Layer 2 Docker images #####"
    rebuild_docker
fi
