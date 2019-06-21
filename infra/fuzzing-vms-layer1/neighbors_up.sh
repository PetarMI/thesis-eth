#!/bin/bash

readonly NEIGHBOR_LOGS="${HOME}/logs/neighbors.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')

function check_neighbor_discovery {
    while read -r cont
    do
        local real_neighbors=$(cat ${NEIGHBOR_LOGS} | grep ${cont} | awk '{print $2}')
        local num_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "${IP_regex}" | wc -l)

        while [[ "real_neighbors" -gt "num_neighbors" ]]; do
            sleep 1
            num_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "${IP_regex}" | wc -l)
        done
    done <<< ${containers}
}

check_neighbor_discovery