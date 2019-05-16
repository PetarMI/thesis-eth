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

echo "1/2 Load FRR image"
start=$SECONDS
docker load -i ${FRR_IMAGE}
signal_fail $? "Loading FRR image"
duration=$(( SECONDS - start ))
echo "Load time: ${duration}"

echo "2/2 Setting up FRR container"
start=$SECONDS
docker run -itd --privileged --name frr --network host frr:6.0.2
signal_fail $? "Running an FRR container"
duration=$(( SECONDS - start ))
echo "Setup time: ${duration}"
