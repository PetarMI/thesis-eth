#!/bin/bash

readonly ROUTES_LOGS="${HOME}/logs/run_routes.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

readonly MAX_ATTEMPTS=6
readonly WAIT_INTERVAL=1

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')

function check_routes_up {
    while read -r cont
    do
        local prev_routes=$(cat ${ROUTES_LOGS} | grep ${cont} | awk '{print $2}')
        local num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')

        local attempts=0

        while true ; do
            if [[ "num_routes" -ge "prev_routes" ]]; then
                break
            elif [[ "$attempts" -ge "$MAX_ATTEMPTS" ]]; then
                echo "INFO: Container ${cont} on VM ${HOSTNAME} timed out"
                break
            fi

            sleep ${WAIT_INTERVAL}
            attempts=$(( $attempts + 1 ))
            num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')
        done
    done <<< ${containers}
}

check_routes_up
