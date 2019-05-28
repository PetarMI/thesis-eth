#!/bin/bash

ARG_state="undefined"
ARG_interface="undefined"

while getopts "s:i:" option
do
    case "${option}" in
        s) ARG_state="$OPTARG";;
        i) ARG_interface="$OPTARG";;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure an option has been entered
if [[ "${ARG_state}" == "undefined" ]]; then
    echo "Please specify up (-srestore) or down (-d)"
    exit 1
fi

#######################################
# Script logic
#######################################
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed with exit code ${exit_code} ${msg}${NC}\n"
        exit ${exit_code}
    fi
}

if [[ ${ARG_state} == "drop" ]]
then
    docker exec frr vtysh -c "configure terminal" -c "interface ${ARG_interface}" -c "shutdown"
elif [[ ${ARG_state} == "restore" ]]
then
    docker exec frr vtysh -c "configure terminal" -c "interface ${ARG_interface}" -c "no shutdown"
else
    signal_fail 1 "Unknown link state"
fi
