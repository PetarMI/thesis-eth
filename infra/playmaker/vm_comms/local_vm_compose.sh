#!/bin/bash

usage="Script to ssh into VM and call compose scripts

where:
    --up       compose UP
    --down     compose DOWN
    --help     show this help text"

UP=3

while [[ "$1" != "" ]]; do
    case $1 in
        -u | --up)              shift
                                UP=1
                                ;;
        -d | --down )           UP=0
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        *)                      echo "Unknown flag"
                                exit
                                ;;
    esac
    shift
done

# make sure a topology file has been entered
if [[ ${UP} == 3 ]]; then
        echo "Please specify --up or --down"
        exit 1
fi

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

printf "${RED}Implement -up or -down argument${NC}\n"

function compose_up {
    printf "${RED}Implement compose-up${NC}\n"
}

function compose_down {
    printf "${RED}Implement compose-down${NC}\n"
}

#######################################
# Actual script logic
#######################################

if [[ ${UP} == 1 ]]
then
    echo "### Compose UP ###"
    compose_up
elif [[ ${UP} == 0 ]]
then
    echo "### Compose DOWN ###"
    compose_down
fi
