#!/bin/bash
#
# Extract the next hop info at a specific device for a specific destination
#
# Input:
#   - VM IP on which the source container is residing - ex. 192.168.56.10
#   - source container name
#   - destination network in the form of network IP/netmask (ex. 10.0.2.0/24)
#
# Output:
#   - Comma separated string of IP addresses
#       - first one (if any) is the network IP without a netmask
#       - all others are next hop IP addresses specified without netmask

vm_ip="$1"
container_name="$2"
dest_net="$3"

L2_fib_sh="/home/api/fib_paths.sh"
readonly USER="fuzzvm"
readonly IP_regex="([0-9]{1,3}[\.]){3}[0-9]{1,3}"

# get the FIB info for that path
command="docker exec ${container_name} ${L2_fib_sh} -d ${dest_net}"
fib=$(ssh -n -T "${USER}@${vm_ip}" "${command}")

ips=$(echo "${fib}" | grep -E -o "${IP_regex}")

formatted_ips=$(echo "${ips}" | awk -vORS=, '{ print $1 }' | sed 's/,$/\n/')

echo -n "${formatted_ips}"
