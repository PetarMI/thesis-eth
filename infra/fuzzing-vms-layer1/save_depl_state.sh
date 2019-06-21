#!/bin/bash

readonly HOME_DIR="${HOME}"
readonly NEIGHBOR_LOGS="${HOME}/logs/neighbors.log"
readonly ROUTES_LOGS="${HOME}/logs/routes.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"

readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

containers=$(docker ps | grep phynet | awk '{print $NF}')

function log_neighbors {
    while read -r cont
    do
        num_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "${IP_regex}" | wc -l)
        echo "${cont} ${num_neighbors}" >> ${NEIGHBOR_LOGS}
    done <<< ${containers}
}

function log_routes {
    while read -r cont
    do
        num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')
        echo "${cont} ${num_routes}" >> ${ROUTES_LOGS}
    done <<< ${containers}
}

log_neighbors
log_routes
