#!/bin/bash

FLAG_interfaces=0
FLAG_neighbors=0
FLAG_fib=0
FLAG_routes=0

while getopts "infr" option
do
    case "${option}" in
        i) FLAG_interfaces=1;;
        n) FLAG_neighbors=1;;
        f) FLAG_fib=1;;
        r) FLAG_routes=1;;
        *) echo "Unknown option"; exit 1;;
    esac
done

if [[ ${FLAG_neighbors} == 1 ]]; then
    docker exec frr vtysh -c "show ip ospf neighbor"
elif [[ ${FLAG_fib} == 1 ]]; then
    docker exec frr vtysh -c "show ip fib"
elif [[ ${FLAG_interfaces} == 1 ]]; then
    docker exec frr vtysh -c "show interface"
elif [[ ${FLAG_routes} == 1 ]]; then
    docker exec frr vtysh -c "show ip route summary"
fi
