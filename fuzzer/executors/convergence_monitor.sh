#!/bin/bash

function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        exit ${exit_code}
    fi
}

sleep 2