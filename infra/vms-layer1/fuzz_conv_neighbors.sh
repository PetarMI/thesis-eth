#!/bin/bash

# colors for output
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly NC='\033[0m' # No Color

readonly FRR_INFO_SH="/home/api/device_info.sh"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

readonly MAX_ATTEMPTS=50
readonly WAIT_INTERVAL=2

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')
declare -A slow_containers

function check_neighbours {
    local non_converged=0

    while read -r cont
    do
        local neighbors_info=$(docker exec ${cont} ${FRR_INFO_SH} -n)
        local num_neighbors=$(echo "${neighbors_info}" | grep -E "${IP_regex}" | wc -l)
        local full_neighbors=$(echo "${neighbors_info}" | grep -E "Full" | wc -l)

        if [[ "$num_neighbors" -gt "$full_neighbors" ]]; then
            non_converged=$(( non_converged + 1 ))
            # put the non-ready containers in an associative array
            slow_containers["$cont"]=${num_neighbors}
        fi
    done <<< ${containers}

    return ${non_converged}
}

function double_check_neighbours {
    local non_converged=0

    for cont in "${!slow_containers[@]}"; do
        local full_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "Full" | wc -l)

        local attempts=0
        while true ; do
            if [[ "${slow_containers[$cont]}" -le "$full_neighbors" ]]; then
                echo "INFO: Container ${cont} converged on attempt ${attempts}"
                break
            elif [[ "$attempts" -ge "$MAX_ATTEMPTS" ]]; then
                echo "INFO: Container ${cont} on VM ${HOSTNAME} has non-ready adjacencies"
                non_converged=$(( non_converged + 1 ))
                break
            fi

            sleep ${WAIT_INTERVAL}
            attempts=$(( $attempts + 1 ))
            full_neighbors=$(docker exec ${cont} ${FRR_INFO_SH} -n | grep -E "Full" | wc -l)
        done
    done

    return ${non_converged}
}

# do a one pass over every container's neighbours and store the ones who
# don't have state Full/*
# double check every container for a MAX number of retries
check_neighbours
failed=$?

if [[ "$failed" -gt 0 ]]; then
    double_check_neighbours
    failed=$?

    if [[ "$failed" -gt 0 ]]; then
        printf "${YELLOW}VM: ${HOSTNAME} - ${failed} OSPF neighbors may have failed to converge${NC}\n"
    else
        printf "${GREEN}VM: ${HOSTNAME} - OSPF neighbours converged after double checking${NC}\n"
    fi
else
    printf "${GREEN}VM: ${HOSTNAME} - OSPF neighbours converged on first pass${NC}\n"
fi
