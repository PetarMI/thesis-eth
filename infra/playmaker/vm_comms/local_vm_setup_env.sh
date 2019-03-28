#!/bin/bash

# handle arguments
usage="Script to setup everything needed inside the VMs

where:
    --topology The name of the topology to be deployed
    --help     show this help text"

TOPO=

while [[ "$1" != "" ]]; do
    case $1 in
        -t | --topology)        shift
                                TOPO=$1
                                ;;
        -h | --help )           echo "$usage"
                                exit
                                ;;
        *)                      echo "Unknown flag"
                                exit
                                ;;
    esac
    shift
done

# paths on VM
readonly WORK_DIR="/home/osboxes"
readonly COMPOSE_DIR="/compose/"
readonly DOCKER_DIR="/phynet"
readonly SCRIPT_DIR="/scripts/"

readonly NET_FILE="topo_networks.csv"
readonly CONTAINERS_FILE="topo_containers.csv"
readonly LINKS_FILE="topo_links.csv"

# paths on localhost
readonly PROJ_DIR="/home/pesho/D/thesis-repo/infra"
readonly PHYNET_DIR="${PROJ_DIR}/phynet-layer2"
readonly CSV_DIR="${PROJ_DIR}/playmaker/build_instr/${TOPO}"

#
readonly CONF_FILE="local_vm.conf"
readonly MACHINE="osboxes@localhost"

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

function check_success {
    local exit_code=$1
    local msg=$2

    printf "${msg}..."

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}Success${NC}\n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}\n"
        exit ${exit_code}
    fi
}

function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

function setup_dir_structure {
    echo "TODO - Ensure VM has all necessary folders to copy into"

    while IFS=, read -r idx port role
    do
ssh -T -p ${port} ${MACHINE} << EOF
    rm -r compose/*
EOF
    done < ${CONF_FILE}
}

function upload_compose_files {
    while IFS=, read -r idx port role #|| [ -n "${cont_name}" ]
    do
        local src_nets="${CSV_DIR}/net-compose.csv"
        scp -P ${port} ${src_nets} "${MACHINE}:${WORK_DIR}${COMPOSE_DIR}${NET_FILE}"
        signal_fail $? "Copying networks file"

        local src_conts="${CSV_DIR}/netvm${idx}_containers.csv"
        scp -P ${port} ${src_conts} "${MACHINE}:${WORK_DIR}${COMPOSE_DIR}${CONTAINERS_FILE}"
        signal_fail $? "Copying containers file"

        local src_links="${CSV_DIR}/netvm${idx}_links.csv"
        scp -P ${port} ${src_links} "${MACHINE}:${WORK_DIR}${COMPOSE_DIR}${LINKS_FILE}"
        signal_fail $? "Copying links file"
    done < ${CONF_FILE}
}

function update_docker_files {
    while IFS=, read -r idx port role
    do
        src_scripts="${PHYNET_DIR}/scripts"
        scp -r -P ${port} ${src_scripts} "${MACHINE}:${WORK_DIR}${DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet scripts to VM ${idx}"

        src_docker="${PHYNET_DIR}/Dockerfile"
        scp -P ${port} ${src_docker} "${MACHINE}:${WORK_DIR}${DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet Dockerfile to VM ${idx}"
    done < ${CONF_FILE}
}

echo "### Setting up directory structure on VMs ###"
#setup_dir_structure

echo "### Sending phynet files to VMs ###"
# update_docker_files

echo "### Sending compose files to VMs ###"
upload_compose_files
# echo "${INPUT_DIR}"