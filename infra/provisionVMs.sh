#!/bin/bash

# all stuff about script parameters
usage="$(basename "$0") [-h] [-n n] -- script to provision local VMs via docker-machine commands

where:
    -n  number of VMs to provision (default: 2)
    -h  show this help text"

vms=2

while [[ "$1" != "" ]]; do
    case $1 in
        -n | --numvms )         shift
                                vms=$1
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
    esac
    shift
done

readonly DM="docker-machine"
readonly VM_BASE_NAME="netvm"

function provision_vms {
    for i in $(seq ${vms})
    do
        local vm_name="${VM_BASE_NAME}${i}"
        docker-machine create --driver virtualbox ${vm_name}
    done
}

# make the local machine the swarm manager
function init_swarm_local {
    # first get the IP address for the swarm manager
    local ip=$(ip -f inet addr show vboxnet0 | grep -Po 'inet \K[\d.]+')

    # initiate the swarm and discard stdout
    docker swarm init --advertise-addr ${ip} 1>/dev/null
}

join_instr=

function get_join_instr {
    join_instr=$(docker swarm join-token $1 | grep "docker")
}

# mkdir logs/
# provision_vms
# docker-machine ls
init_swarm_local
get_join_instr "worker"
echo ${join_instr}