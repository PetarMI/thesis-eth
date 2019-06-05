#!/bin/bash

readonly FRR_INFO_SH="/home/api/device_info.sh"

readonly MAX_ATTEMPTS=2
readonly WAIT_INTERVAL=1

# parse the dropped links
raw_dropped_links="$1"
IFS=',' read -r -a dropped_links <<< "$raw_dropped_links"

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')
slow_containers=()

# colors for output
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly NC='\033[0m' # No Color

function check_dropped {
    local non_converged=0

    while read -r cont
    do
        local fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)

        for dlink in "${dropped_links[@]}"
        do
            local in_fib=$(echo "${fib_info}" | grep -E "10.0.1.0" | wc -l)

            if [[ "$in_fib" -ne 0 ]]; then
                non_converged=$(( non_converged + 1 ))
                slow_containers+=("${cont}")
                break
            fi
        done
    done <<< ${containers}

    return ${non_converged}
}

function double_check_dropped {
    # Hopefully we will never come here
    local non_converged=0

    for cont in "${slow_containers[@]}"
    do
        local fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)

	    for dlink in "${dropped_links[@]}"
        do
            local attempts=0
            local failed=0
            # repeat until dropped entry disappears or we reach max attempts
	        while true ; do
                local in_fib=$(echo "${fib_info}" | grep -E "${dlink}" | wc -l)

                if [[ "$in_fib" -eq 0 ]]; then
                    echo "INFO: Container ${cont} dropped link ${dlink} after ${attempts} attempts"
                    break
                elif [[ "$attempts" -ge "$MAX_ATTEMPTS" ]]; then
                    echo "INFO: Container ${cont} still has an entry to ${dlink}"
                    non_converged=$(( non_converged + 1 ))
                    failed=1
                    break
                fi

                attempts=$(( $attempts + 1 ))
                sleep ${WAIT_INTERVAL}
                fib_info=$(docker exec ${cont} ${FRR_INFO_SH} -f)
            done

            # give up on this container entirely and dont check the other links
            if [[ "$failed" -gt 0 ]]; then
                break
            fi
        done
    done

    return ${non_converged}
}


check_dropped
failed=$?

if [[ "$failed" -gt 0 ]]; then
    double_check_dropped
    failed=$?

    if [[ "$failed" -gt 0 ]]; then
        printf "${YELLOW}VM: ${HOSTNAME} - ${failed} devices may have failed to drop failed link from FIB${NC}\n"
    else
        printf "${GREEN}VM: ${HOSTNAME} - Devices dropped failed links from FIB after double checking${NC}\n"
    fi
else
    printf "${GREEN}VM: ${HOSTNAME} - Devices dropped failed links from FIB${NC}\n"
fi

