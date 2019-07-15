#!/bin/bash

#readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"
#
#raw_fib=$(docker exec frr vtysh -c "show ip fib")
#
#connected=$(echo "${raw_fib}" | grep "connected" |  grep -E -o "${IP_regex}" | awk -vORS=, '{ print $1 }' | sed 's/,$/\n/')
#
#via=$(echo "${raw_fib}" | grep "] via" |  grep -E -o "${IP_regex}" | awk -vORS=, '{ print $1 }' | sed 's/,$/\n/')
#
#echo "${via}"

docker exec frr vtysh -c "show ip fib json"