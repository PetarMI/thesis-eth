#!/bin/bash
#
# Script containing functions that check and setup the VM environment

#######################################
# Handle script arguments
#######################################
usage="Script for checking and setting up the VM environment

where:
    -i     check if everything is installed
    -c     clean VM dirs
    -d     setup dir structure
    -p     rebuild the Layer 2 image
    -v     view Dir structure
    -h     show this help text"

FLAG_installed=0
FLAG_clean=0
FLAG_dirs=0
FLAG_build_phynet=0
FLAG_view=0

while getopts "icdpvh" option
do
    case "${option}" in
        i) FLAG_installed=1;;
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
# readonly VM_WORK_DIR="/home/osboxes"
readonly VM_COMPOSE_DIR="compose"
readonly VM_DOCKER_DIR="phynet"
readonly VM_SCRIPT_DIR="vm_scripts"
readonly VM_CONFIG_DIR="device_configs"

# VM info
readonly CONF_FILE="running_vms.conf"
readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

function check_installed {
    while IFS=, read -r idx vm_ip role
    do
	echo "${idx}"
        ssh -n -T "${USER}@${vm_ip}" "sysctl net.ipv4.conf.all.rp_filter"
    done < ${CONF_FILE}
}

function clean {
    while IFS=, read -r idx vm_ip role
    do
ssh -T "${USER}@${vm_ip}" << EOF
    rm -rf */
EOF
    done < ${CONF_FILE}
}

function setup_dir_structure {
    while IFS=, read -r idx vm_ip role
    do
ssh -T "${USER}@${vm_ip}" << EOF
    mkdir -p ${VM_COMPOSE_DIR}
    mkdir -p ${VM_DOCKER_DIR}
    mkdir -p ${VM_SCRIPT_DIR}
    mkdir -p ${VM_CONFIG_DIR}
EOF
    done < ${CONF_FILE}

    echo "## Created directories:"
    printf "${GREEN}/${VM_COMPOSE_DIR}${NC} - store compose files for the particular VM\n"
    printf "${GREEN}/${VM_DOCKER_DIR}${NC} - store Layer 2 Dockerfile and scripts\n"
    printf "${GREEN}/${VM_SCRIPT_DIR}${NC} - store Layer 1 scripts\n"
    printf "${GREEN}/device_configs${NC} - store config files for all topology devices\n"
    echo "## Dirs created during upload"
    printf "${GREEN}/phynet/scripts${NC} - store the Layer 2 scripts\n"
}

function view {
    while IFS=, read -r idx vm_ip role
    do
        if [[ ${role} == "manager" ]]
        then
ssh -T "${USER}@${vm_ip}" << EOF
    cd ${VM_DOCKER_DIR}
    ls
EOF
            break
        fi
    done < ${CONF_FILE}
}

#######################################
# Rebuild the Layer 2 Docker image on every VM
#######################################
function rebuild_docker {
    while IFS=, read -r idx vm_ip role
    do
        echo "## Rebuilding L2 image on VM ${idx} ##"
ssh -T "${USER}@${vm_ip}" <<- 'EOF'
    docker images | grep phynet | awk '{print $3}' | xargs docker rmi
    cd phynet/
    docker build --rm -t phynet:latest .
EOF
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################
if [[ ${FLAG_installed} == 1 ]]; then
    printf "${CYAN}#### Verifying installation prerequisites ####${NC}\n"
    check_installed
fi

if [[ ${FLAG_clean} == 1 ]]; then
    printf "${CYAN}#### Cleaning VM directories ####${NC}\n"
    clean
fi

if [[ ${FLAG_dirs} == 1 ]]; then
    printf "${CYAN}#### Building VM dir structure ####${NC}\n"
    setup_dir_structure
    check_installed
fi

if [[ ${FLAG_view} == 1 ]]; then
    printf "${CYAN}#### View VM dir structure ####${NC}\n"
    view
fi

if [[ ${FLAG_build_phynet} == 1 ]]; then
    printf "${CYAN}#### Rebuilding Layer 2 Docker images ####${NC}\n"
    rebuild_docker
fi
