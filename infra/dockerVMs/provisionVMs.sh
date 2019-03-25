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

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

readonly DM="docker-machine"
readonly VM_BASE_NAME="netvm"
readonly DIR=$(echo $PWD)

function check_success {
    local exit_code=$1
    local msg=$2

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}Success:${NC} ${msg}\n"
    fi
}

function check_fail {
    local exit_code=$1
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}\n"
    fi
}

function provision_vms {
    local pids=()

    for i in $(seq ${vms})
    do
        local vm_name="${VM_BASE_NAME}${i}"
        docker-machine create --driver virtualbox ${vm_name} 1>${DIR}/logs/provision_${vm_name}.log
        check_success $? "${vm_name} created"
    done
}

#declare -A vm_data
vm_names=()

function save_vm_data {
    vm_raw=$(docker-machine ls | grep "virtualbox" | awk '{print $1, $5}')

    while read name raw_ip
    do
        #vm_data[${name}]=$(echo "${raw_ip}" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
        vm_names+=(${name})
    done <<< "${vm_raw}"
}

#fucntion save_to_csv {
#
#}

# make the local machine the swarm manager
function init_swarm_local {
    # first get the IP address for the swarm manager
    local ip=$(ip -f inet addr show vboxnet0 | grep -Po 'inet \K[\d.]+')

    # initiate the swarm and discard stdout
    docker swarm init --advertise-addr ${ip} 1>${DIR}/logs/swarm_init.log
}

join_instr=

function get_join_instr {
    local node_type=$1
    join_instr=$(docker swarm join-token ${node_type} | echo $(grep "docker"))
}

function join_swarm {
    for vm in "${vm_names[@]}"
    do
        get_join_instr "worker"
        docker-machine ssh ${vm} "${join_instr}" 1>>${DIR}/logs/swarm_join.log
        check_success $? "${vm} joined swarm"
    done
}

mkdir logs/

echo "1/4 Provisioning VMs"
provision_vms
check_fail $?

echo "2/4 Reading VM data"
save_vm_data
check_fail $?

echo "3/4 Initializing swarm on local machine"
init_swarm_local
check_fail $?

echo "4/4 Join VMs to swarm"
join_swarm
check_fail $?

docker node ls
