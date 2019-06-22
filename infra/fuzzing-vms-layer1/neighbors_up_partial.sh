#!/bin/bash

readonly NEIGHBOR_LOGS="${HOME}/logs/run_neighbors.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

# parse the restored links
raw_containers="$1"
IFS=',' read -r -a restored_containers <<< "$raw_containers"

function check_neighbor_discovery {
    for cont in "${restored_containers[@]}"
    do
        # the log file is updated after every drop in StateTransition.py
        local prev_neighbors=$(cat ${NEIGHBOR_LOGS} | grep ${cont} | awk '{print $2}')

        # check that the container in the argument list belongs to this VM
        if [[ ${prev_neighbors} == "" ]]; then
            continue
        fi

        local num_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "${IP_regex}" | wc -l)

        # Number of current neighbors has to be larger than the number stored after the drop
        while [[ "$prev_neighbors" -ge "$num_neighbors" ]]; do
            sleep 1
            num_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "${IP_regex}" | wc -l)
        done
    done
}

check_neighbor_discovery
