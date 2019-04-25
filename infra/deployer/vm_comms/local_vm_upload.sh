#!/bin/bash
#
# Copy all necessary files into the VMs

#######################################
# Handle script arguments
#######################################
usage="Script to upload all needed files on the VMs

where:
    -t  The name of the topology to be deployed
    -a  Upload all files
    -c  Upload compose files
    -s  Upload VM scripts
    -d  Upload docker files
    -f  Upload device configs
    -h  Show this help text"

FLAG_topology="youforgottopassatopologyname"
FLAG_compose_files=0
FLAG_docker_files=0
FLAG_vm_scripts=0
FLAG_device_configs=0

while getopts "t:acsdfh" option
do
    case "${option}" in
        t) FLAG_topology=${OPTARG};;
        a) FLAG_compose_files=1
           FLAG_docker_files=1
           FLAG_vm_scripts=1;;
        c) FLAG_compose_files=1;;
        s) FLAG_vm_scripts=1;;
        d) FLAG_docker_files=1;;
        f) FLAG_device_configs=1;;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure a topology file has been entered
if [[ ${FLAG_topology} == "youforgottopassatopologyname" ]]; then
        echo "Please topology via -t"
        exit 1
fi

#######################################
# Define all paths
#######################################
# VM paths
# readonly VM_WORK_DIR="/home/osboxes"
readonly VM_COMPOSE_DIR="/compose"
readonly VM_DOCKER_DIR="/phynet"
readonly VM_SCRIPT_DIR="/vm_scripts"

# compose files
readonly VM_NET_FILE="${VM_COMPOSE_DIR}/topo_networks.csv"
readonly VM_CONTAINERS_FILE="${VM_COMPOSE_DIR}/topo_containers.csv"
readonly VM_LINKS_FILE="${VM_COMPOSE_DIR}/topo_links.csv"

# Local paths
readonly PM_HOME_DIR="$HOME"
readonly PM_WORK_DIR="${PM_HOME_DIR}/thesis-eth/infra"
readonly PM_DOCKER_DIR="${PM_WORK_DIR}/phynet-layer2"
readonly PM_SCRIPT_DIR="${PM_WORK_DIR}/vms-layer1"
readonly PM_DEPLOY_DIR="${PM_WORK_DIR}/deployer/deployment_files/${FLAG_topology}"
readonly PM_COMPOSE_DIR="${PM_DEPLOY_DIR}/compose_files"

# VM info
readonly CONF_FILE="local_vm.conf"
readonly USER="fuzzvm"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

#######################################
# Display success or failure of the last executed process
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function check_success {
    local exit_code=$1
    local msg=$2

    if [[ ${exit_code} == 0 ]]; then
        printf "${GREEN}Success:${NC} ${msg}\n"
    else
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

#######################################
# Only signal if the last executed process failed
# Arguments:
#   exit_code: The exit code of the last process
#   msg:       String describing the process
#######################################
function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

#######################################
# Upload all files necessary to do a compose up on the VM
#   - networks at the Swarm manager
#   - containers to be started at each VM
#   - links for every container
#######################################
function upload_compose_files {
    while IFS=, read -r idx vm_ip role
    do
        local src_nets="${PM_COMPOSE_DIR}/net-compose.csv"
        scp ${src_nets} "${USER}@${vm_ip}:.${VM_NET_FILE}" 1>/dev/null
        signal_fail $? "Copying networks file to VM ${idx}"

        local src_conts="${PM_COMPOSE_DIR}/netvm${idx}_containers.csv"
        scp ${src_conts} "${USER}@${vm_ip}:.${VM_CONTAINERS_FILE}" 1>/dev/null
        signal_fail $? "Copying containers file to VM ${idx}"

        local src_links="${PM_COMPOSE_DIR}/netvm${idx}_links.csv"
        scp ${src_links} "${USER}@${vm_ip}:.${VM_LINKS_FILE}" 1>/dev/null
        signal_fail $? "Copying links file to VM ${idx}"

        check_success 0 "Uploaded to VM ${idx} "
    done < ${CONF_FILE}
}

#######################################
# Upload all Layer 2 related files
#   - Phynet image Dockerfile
#   - Scripts residing in each Layer 2 container (API)
#######################################
function upload_docker_files {
    while IFS=, read -r idx vm_ip role
    do
        local src_scripts="${PM_DOCKER_DIR}/api"
        scp -r ${src_scripts} "${USER}@${vm_ip}:.${VM_DOCKER_DIR}" 1>/dev/null
        check_success $? "Uploaded Phynet scripts to VM ${idx}"

        local src_docker="${PM_DOCKER_DIR}/Dockerfile"
        scp ${src_docker} "${USER}@${vm_ip}:.${VM_DOCKER_DIR}" 1>/dev/null
        check_success $? "Uploaded Phynet Dockerfile to VM ${idx}"
    done < ${CONF_FILE}
}

#######################################
# Upload the scripts that are run on the VMs
#   - compose_up.sh to deploy Layer 2 networks and containers
#######################################
function upload_vm_scripts {
    while IFS=, read -r idx vm_ip role
    do
        local src_scripts="${PM_SCRIPT_DIR}"
        scp ${src_scripts}/* "${USER}@${vm_ip}:.${VM_SCRIPT_DIR}/" 1>/dev/null
        check_success $? "Uploaded to VM ${idx}"
    done < ${CONF_FILE}
}

#######################################
# Upload the scripts that are run on the VMs
#   - compose_up.sh to deploy Layer 2 networks and containers
#######################################
function upload_device_configs {
    while IFS=, read -r idx vm_ip role
    do
        local src_configs="${PM_DEPLOY_DIR}/device_configs"
        scp -r ${src_configs} "${USER}@${vm_ip}:./" 1>/dev/null
        check_success $? "Uploaded to VM ${idx}"
    done < ${CONF_FILE}
}

#######################################
# Actual script logic
#######################################
echo "##### Uploading files to VMs #####"

if [[ ${FLAG_compose_files} == 1 ]]; then
    echo "### Uploading compose files to VMs ###"
    upload_compose_files
fi

if [[ ${FLAG_docker_files} == 1 ]]; then
    echo "### Uploading Layer 2 Docker files to VMs ###"
    upload_docker_files
fi

if [[ ${FLAG_vm_scripts} == 1 ]]; then
    echo "### Uploading VM scripts to VMs ###"
    upload_vm_scripts
fi

if [[ ${FLAG_device_configs} == 1 ]]; then
    echo "### Uploading device configs to VMs ###"
    upload_device_configs
fi
