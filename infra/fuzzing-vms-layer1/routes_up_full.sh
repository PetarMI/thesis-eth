#!/bin/bash

readonly ROUTES_LOGS="${HOME}/logs/routes.log"
readonly FRR_INFO_SH="/home/api/device_info.sh"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

# collect all running container names
containers=$(docker ps | grep phynet | awk '{print $NF}')

function check_routes_up {
    while read -r cont
    do
        local real_routes=$(cat ${ROUTES_LOGS} | grep ${cont} | awk '{print $2}')
        local num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')

        while [[ "$real_routes" -gt "$num_routes" ]]; do
            sleep 1
            num_routes=$(docker exec ${cont} ${FRR_INFO_SH} -r | grep "Totals" | awk '{print $2}')
        done
    done <<< ${containers}
}

check_routes_up
