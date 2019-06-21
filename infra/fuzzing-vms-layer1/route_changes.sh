#!/bin/bash

readonly HOME_DIR="${HOME}"
readonly ROUTES_LOGS="${HOME}/logs/run_routes.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"

containers=$(docker ps | grep phynet | awk '{print $NF}')

function log_routes {
    > ${ROUTES_LOGS}

    while read -r cont
    do
        local num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')
        echo "${cont} ${num_routes}" >> ${ROUTES_LOGS}
    done <<< ${containers}
}

function check_changes {
    while read -r cont
    do
        local prev_routes=$(cat ${ROUTES_LOGS} | grep ${cont} | awk '{print $2}')
        local num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')

        if [[ "$prev_routes" -ne "$num_routes" ]]; then
            echo "Detected route change: Old: ${prev_routes} New: ${num_routes}"
            return 1
        fi
    done <<< ${containers}

    return 0
}

MAX_ITERATIONS=6
readonly WAIT_INTERVAL=1
readonly REDUCED_ITERATIONS=4
attempts=0

log_routes

while [[ "$MAX_ITERATIONS" -gt "$attempts" ]]; do
    check_changes
    changes=$?

    if [[ "$changes" -gt 0 ]]; then
        log_routes
        attempts=0
        MAX_ITERATIONS=$REDUCED_ITERATIONS
    else
        attempts=$(( $attempts + 1 ))
    fi

    sleep ${WAIT_INTERVAL}
done
