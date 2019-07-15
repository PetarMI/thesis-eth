#!/bin/bash
#
# Extract the FIB of a specific device


vm_ip="$1"
container_name="$2"

L2_fib_sh="/home/api/fib_info.sh"
readonly USER="fuzzvm"

# get the FIB info for that path
command="docker exec ${container_name} ${L2_fib_sh}"
fib=$(ssh -n -T "${USER}@${vm_ip}" "${command}")

echo -n "${fib}"
