#!/bin/bash

#######################################
# Handle script arguments
#######################################
usage="Script to perform NAT

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
readonly DPL_LOG_DIR="${DEPLOY_DIR}/net_logs"

# files
readonly SUBNETS_FILE="${DEPLOY_DIR}/nat_files/matched-subnets.csv"
readonly IFACES_SIM_FILE="${DEPLOY_DIR}/nat_files/sim_ifaces.csv"
readonly IFACES_ORIG_FILE="${DEPLOY_DIR}/nat_files/orig_ifaces.csv"

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
# Read all config files' filenames into an array
#######################################
config_files=()

function read_config_files {
    while IFS= read -r line; do
        config_files+=( "$line" )
    done < <( find ${DPL_CONFIG_DIR} -type f )
}

#######################################
# Read all config files' filenames into an array
#######################################
iface_files=()

function read_iface_log_files {
    while IFS= read -r line; do
        iface_files+=( "$line" )
    done < <( find ${DPL_LOG_DIR} -type f -name 'ipa*')
}

function parse_device_configs {
    rm -f ${IFACES_ORIG_FILE}

    for f in "${config_files[@]}"
    do
        # get just the filename
        local filename=$(echo ${f##*/})
        filename=$(echo ${filename%.*})
        grep -E '(^interface|ip address)' ${f} | sed '$!N;s/\n/,/' \
        | awk '{print $2 $5}' | sed -e "s/^/$filename,/" >> ${IFACES_ORIG_FILE}
        signal_fail $? "Processing ${f}"
    done
}

#######################################
# Pair iface and ip address of only relevant ifaces
# Output:
#   - /nat_files/sim_ifaces.csv
#######################################
function parse_iface_logs {
    rm -f ${IFACES_SIM_FILE}

    for f in "${iface_files[@]}"
    do
        # get just the filename
        local filename=$(echo ${f##*_})
        filename=$(echo ${filename%.*})
        # pair every two lines
        sed '$!N;s/\n/,/' ${f} | sed '/10.0./!d' \
        | sed -e "s/^/${filename},/" >> ${IFACES_SIM_FILE}
        signal_fail $? "Processing ${f}"
    done
}

#######################################
# Invoke python script to perform subnet matching and all
# Output:
#   - /nat_files/matched-subnets.csv
#######################################
function match_subnets {
    python NatController.py -t ${FLAG_topology}
}

#######################################
# Perform the subnet substitution in every file
# Output:
#   - updated /device_configs/*.conf
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
echo "#### Pre-processing logs ####"
copy_files
read_config_files
read_iface_log_files
parse_iface_logs
parse_device_configs
echo "#### Performing network matching ####"
match_subnets
echo "#### Performing NAT ####"
echo "## Updating subnets ##"
#sed_subnets


