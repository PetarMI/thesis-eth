#!/bin/bash
#
# Script containing functions that check and setup the VM environment

#######################################
# Handle script arguments
#######################################
usage="Script for checking and setting up the VM environment

where:
    -d     rebuild the Layer 2 image
    -h     show this help text"

FLAG_build_phynet=0

while getopts "dscih" option
do
    case "${option}" in
        d) FLAG_build_phynet=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# VM info
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

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
# Rebuild the Layer 2 Docker image on every VM
#######################################
function rebuild_docker {
    printf "${RED}Building Layer 2 container not implemented${NC}\n"
}

if [[ ${FLAG_build_phynet} == 1 ]]; then
    echo "##### Rebuilding Layer 2 Docker images #####"
    rebuild_docker
fi