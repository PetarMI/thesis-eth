#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to upload all needed files on the VMs

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

#######################################
# Declare static paths
#######################################
readonly WORK_DIR="/home/pesho/D/thesis-repo"
readonly CONFIG_DIR="${WORK_DIR}/topologies/${FLAG_topology}/device_configs"
readonly DEPLOY_DIR="${WORK_DIR}/infra/deployer/deployment_files/${FLAG_topology}"
readonly DPL_CONFIG_DIR="${DEPLOY_DIR}/device_configs"

# files
readonly SUBNETS_FILE="${DEPLOY_DIR}/nat_files/matched-subnets.csv"

# colors for output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color


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
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${RED}${msg}${NC}\n"
        exit ${exit_code}
    fi
}

#######################################
# Copy the device configs files to deployment dir
#######################################
function copy_files {
    cp -R ${CONFIG_DIR} ${DEPLOY_DIR}
}

#######################################
# Invoke python script to perform subnet matching and all
#######################################
function match_subnets {
    python NatController.py -t ${FLAG_topology}
}

#######################################
# Read all config files' filenames into an array
#######################################
config_files=()

function read_filenames {
    while IFS= read -r line; do
        config_files+=( "$line" )
    done < <( find ${DPL_CONFIG_DIR} -type f )
}

#######################################
# Perform the subnet substitution in every file
#######################################
function sed_subnets {
    for f in "${config_files[@]}"
    do
        while IFS=, read -r old new
        do
            sed -i -e "s%${old}%${new}%g" ${f}
            signal_fail $? "Sed-ing ${f}"
        done < "${SUBNETS_FILE}"
        printf "${GREEN}Translated ${f} ${NC}\n"
    done
}

#######################################
# Actual script logic
#######################################
echo "###### Updating device configurations ######"
echo "#### Performing network matching ####"
match_subnets
copy_files
read_filenames
echo "#### Performing NAT ####"
sed_subnets


