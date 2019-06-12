#!/bin/bash

vm_ip="$1"
container_name="$2"
dest_net="$3"

#while getopts "m:s:d:" option
#do
#    case "${option}" in
#        m) vm_ip="$OPTARG";;
#        s) container_name="$OPTARG";;
#        d) dest_net="$OPTARG";;
#        *) echo "Unknown option"; exit 1;;
#    esac
#done

L2_fib_sh="/home/api/reach_fib.sh"
readonly USER="fuzzvm"

command="docker exec ${container_name} ${L2_fib_sh} -d ${dest_net}"
next_hop=$(ssh -n -T "${USER}@${vm_ip}" "${command}")
echo -n "${next_hop}"

#while true; do
#    command="docker exec ${container_name} ${L2_fib_sh} -d ${dest_net}"
#    next_hop=$(ssh -n -T "${USER}@${vm_ip}" "${command}")
#
#    if [[ ${next_hop} = "connected" ]]; then
#        exit 0
#    elif [[ ${next_hop} = "" ]]; then
#        exit 1
#    else
#        echo "Next hop is ${next_hop}"
#        exit 2
#    fi
#done