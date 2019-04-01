#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script that connects to VMs and does some operation on the containers

where:
    -d     rebuild the Layer 2 image
    -n     remove networks
    -h     show this help text"

FLAG_build_phynet=0
FLAG_networks=0

while getopts "dnh" option
do
    case "${option}" in
        d) FLAG_build_phynet=1;;
        n) FLAG_networks=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac


# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

function build_docker {
    printf "${RED}Building Layer 2 container not implemented${NC}\n"
}

