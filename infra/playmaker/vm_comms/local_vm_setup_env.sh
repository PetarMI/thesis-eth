#!/bin/bash

# handle arguments
usage="Script to setup everything needed inside the VMs

where:
    --topology The topology to be deployed
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
readonly CONTAINER_FILE="topo_containers.csv"
readonly LINKS_FILE="topo_links.csv"

# paths on localhost
readonly CONF_FILE="local_vm.conf"
readonly PROJ_DIR="/home/pesho/D/thesis-repo/infra"


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
        net_compose=
        scp -P ${port} ${INPUT_DIR} "${MACHINE}:"
    done < ${CONF_FILE}
}

function update_docker_files {
    phynet_dir="${PROJ_DIR}/phynet-layer2"

    while IFS=, read -r idx port role
    do
        src="${phynet_dir}/scripts"
        scp -r -P ${port} ${src} "${MACHINE}:${WORK_DIR}${DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet scripts to VM ${idx}"

        src="${phynet_dir}/Dockerfile"
        scp -P ${port} ${src} "${MACHINE}:${WORK_DIR}${DOCKER_DIR}" 1>/dev/null
        check_success $? "Sending Phynet Dockerfile to VM ${idx}"
    done < ${CONF_FILE}
}

echo "### Setting up directory structure on VMs ###"
setup_dir_structure

echo "### Sending phynet files to VMs ###"
# update_docker_files

# echo "${INPUT_DIR}"