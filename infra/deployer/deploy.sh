#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to deploy the whole topology with all the steps

where:
    -t  The name of the topology to be deployed
    -h  Show this help text"

FLAG_topology="youforgottopassatopologyname"

while getopts "t:h" option
do
    case "${option}" in
        t) FLAG_topology=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

# make sure a topology file has been entered
if [[ ${FLAG_topology} == "youforgottopassatopologyname" ]]; then
        echo "Please topology via -t"
        exit 1
fi

readonly HOME_DIR="${HOME}"
readonly DEPLOYER_DIR="${HOME_DIR}/thesis-eth/infra/deployer"
readonly VM_COMMS_DIR="${DEPLOYER_DIR}/vm_comms"
readonly COMPOSER_DIR="${DEPLOYER_DIR}/composer"
readonly NAT_DIR="${DEPLOYER_DIR}/nat"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly L_GREEN='\033[1;32m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color


#######################################
# Only signal if the last executed process failed
#######################################
function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        printf "${RED}Failed with exit code ${exit_code}${NC}\n"
        exit ${exit_code}
    fi
}

printf "${L_GREEN}######### 0/9 Removing old files locally #########${NC}\n"
rm -rf "$DEPLOYER_DIR/deployment_files/${FLAG_topology}"
signal_fail $?

printf "${L_GREEN}######### 1/9 Setting up VM directories #########${NC}\n"
cd "${VM_COMMS_DIR}"
bash ${VM_COMMS_DIR}/local_vm_env.sh -cd
signal_fail $?

printf "${L_GREEN}######### 2/9 Generating compose files #########${NC}\n"
cd "${COMPOSER_DIR}"
python TopoComposer.py -t "${FLAG_topology}"
signal_fail $?

printf "${L_GREEN}######### 3/9 Uploading compose files to VMs #########${NC}\n"
cd "${VM_COMMS_DIR}"
bash local_vm_upload.sh -t "${FLAG_topology}" -a
signal_fail $?

printf "${L_GREEN}######### 4/9 Building Layer 2 on VMs #########${NC}\n"
bash local_vm_compose.sh -u
signal_fail $?

printf "${L_GREEN}######### 5/9 Setup L3 device containers #########${NC}\n"
bash local_vm_configure.sh -s
signal_fail $?

printf "${L_GREEN}######### 6/9 Downloading data #########${NC}\n"
bash local_vm_download.sh -t "${FLAG_topology}"
signal_fail $?

printf "${L_GREEN}######### 7/9 Performing NAT #########${NC}\n"
cd "${NAT_DIR}"
bash perform_nat.sh -t "${FLAG_topology}"
signal_fail $?

printf "${L_GREEN}######### 8/9 Building Layer 2 on VMs #########${NC}\n"
cd "${VM_COMMS_DIR}"
bash local_vm_upload.sh -t "${FLAG_topology}" -f
signal_fail $?

printf "${L_GREEN}######### 9/9 Building Layer 2 on VMs #########${NC}\n"
bash local_vm_configure.sh -c
signal_fail $?
