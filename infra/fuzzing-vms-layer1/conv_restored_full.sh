#!/bin/bash

readonly FRR_INFO_SH="/home/api/device_info.sh"

readonly MAX_ATTEMPTS=30
readonly WAIT_INTERVAL=1

# parse the restored links
raw_restored_links="$1"
IFS=',' read -r -a restored_links <<< "$raw_restored_links"

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')
slow_containers=()

# colors for output
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly NC='\033[0m' # No Color

function check_restored {
    local non_converged=0

    while read -r cont
    do
        local fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)

        for rlink in "${restored_links[@]}"
        do
            local in_fib=$(echo "${fib_info}" | grep -E "${rlink}" | wc -l)

            if [[ "$in_fib" -eq 0 ]]; then
                non_converged=$(( non_converged + 1 ))
                slow_containers+=("${cont}")
                break
            fi
        done
    done <<< ${containers}

    return ${non_converged}
}

function double_check_restored {
    local non_converged=0

    for cont in "${slow_containers[@]}"
    do
        local fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)

	    for rlink in "${restored_links[@]}"
        do
            local attempts=0
            # repeat until restored entry appears or we reach max attempts
	        while true ; do
                local in_fib=$(echo "${fib_info}" | grep -E "${rlink}" | wc -l)

                if [[ "$in_fib" -gt 0 ]]; then
                    echo "INFO: Container ${cont} restored link ${rlink} after ${attempts} attempts"
                    break
                elif [[ "$attempts" -ge "$MAX_ATTEMPTS" ]]; then
                    echo "INFO: Container ${cont} still has NO entry to ${rlink}"
                    non_converged=$(( non_converged + 1 ))
                    break
                fi

                attempts=$(( $attempts + 1 ))
                sleep ${WAIT_INTERVAL}
                fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)
            done
        done
    done

    return ${non_converged}
}


check_restored
failed=$?

if [[ "$failed" -gt 0 ]]; then
    double_check_restored
    failed=$?

    if [[ "$failed" -gt 0 ]]; then
        printf "${YELLOW}VM: ${HOSTNAME} - ${failed} devices may have failed to restore links${NC}\n"
    else
        printf "${GREEN}VM: ${HOSTNAME} - Devices restored links after double checking${NC}\n"
    fi
else
    printf "${GREEN}VM: ${HOSTNAME} - Devices restored links${NC}\n"
fi

