#!/bin/bash

FLAG_failure="undefined"
ARG_vm="undefined"
ARG_container="undefined"
ARG_iface="undefined"
ARG_state="undefined"

while getopts "f:v:d:i:s:" option
do
    case "${option}" in
        f) FLAG_failure="$OPTARG";;
        v) ARG_vm="$OPTARG";;
        d) ARG_container="$OPTARG";;
        i) ARG_iface="$OPTARG";;
        s) ARG_state="$OPTARG";;
        *) echo "Unknown option"; exit 1;;
    esac
done

USER="fuzzvm"
L2_iface_sh="/home/api/iface_state.sh"
L1_ipatbles_sh="undefined"

# colors for output
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Only signal if the last executed process failed
#######################################
function signal_fail {
    local exit_code=$1
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed with exit code ${exit_code}${NC}\n"
        exit ${exit_code}
    fi
}

# Check failure type - interface shutdown or iptables rules
# For now only interface shutdown is supported
if [[ "${FLAG_failure}" == "iface" ]]; then
    command="docker exec ${ARG_container} ${L2_iface_sh} -i ${ARG_iface} -s ${ARG_state}"
    ssh -T "${USER}@${ARG_vm}" "${command}"
    signal_fail $?
else
    printf "${RED}Unimplemented failure type${NC}\n"
    exit 1
fi
