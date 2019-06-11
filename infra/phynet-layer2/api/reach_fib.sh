#!/bin/bash

ARG_destination="undefined"

while getopts "d:" option
do
    case "${option}" in
        d) ARG_destination="$OPTARG";;
        *) echo "Unknown option"; exit 1;;
    esac
done

docker exec frr vtysh -c "show ip fib" | grep -E "${ARG_destination}" | awk '{print $5}' | sed 's/,$//'
