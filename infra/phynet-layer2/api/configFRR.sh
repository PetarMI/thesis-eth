#!/bin/bash

readonly FRR_IMAGE="prefrr.tar"
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

echo "1/3 Copying config files to FRR container"
config_file=$(hostname)
docker cp /home/configs/${config_file}.conf frr:/home/device-config.conf
signal_fail $? "Copying config files to FRR container"

echo "2/3 Setting configs to frr.conf"
docker exec frr bash -c "cp /home/device-config.conf /etc/frr/frr.conf"
signal_fail $? "Setting integrated configs"

echo "3/3 Restart FRR container to load new configs"
docker restart frr 1>/dev/null
signal_fail $? "Restarting FRR container"
