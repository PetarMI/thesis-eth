#!/bin/bash

ARG_destination="undefined"

while getopts "d:" option
do
    case "${option}" in
        d) ARG_destination="$OPTARG";;
        *) echo "Unknown option"; exit 1;;
    esac
done

docker exec frr vtysh -c "show ip fib ${ARG_destination} longer-prefixes"
