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
readonly HOME_DIR="${HOME}"
readonly WORK_DIR="${HOME_DIR}/thesis-eth"
readonly CONFIG_DIR="${WORK_DIR}/topologies/${FLAG_topology}/device_configs"
readonly DEPLOY_DIR="${WORK_DIR}/infra/deployer/deployment_files/${FLAG_topology}"
readonly DPL_CONFIG_DIR="${DEPLOY_DIR}/device_configs"
readonly DPL_LOG_DIR="${DEPLOY_DIR}/net_logs"
readonly DPL_NAT_DIR="${DEPLOY_DIR}/nat_files"

# files
readonly SUBNETS_FILE="${DPL_NAT_DIR}/matched-subnets.csv"
readonly MATCHED_IFACES="${DPL_NAT_DIR}/matched-ifaces.csv"
readonly MATCHED_IPS="${DPL_NAT_DIR}/matched-ips.csv"
readonly IFACES_SIM_FILE="${DPL_NAT_DIR}/sim_ifaces.csv"
readonly IFACES_ORIG_FILE="${DPL_NAT_DIR}/orig_ifaces.csv"

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
        printf "${RED}Failed ${NC}with exit code ${exit_code}: ${RED}${msg}${NC}\n"
        exit ${exit_code}
    fi
}

##############################################################################
######################## READING FILES SECTION ###############################
##############################################################################
# TODO: may need to do some processing on the filenames
function copy_config_files {
    cp -R ${CONFIG_DIR} ${DEPLOY_DIR}
    signal_fail $? "Copying config files"
}

config_files=()

function read_config_files {
    while IFS= read -r line; do
        config_files+=( "$line" )
    done < <( find ${DPL_CONFIG_DIR} -type f )
}

iface_files=()

function read_iface_log_files {
    while IFS= read -r line; do
        iface_files+=( "$line" )
    done < <( find ${DPL_LOG_DIR} -type f -name 'ipa*')
}

#######################################
# Ensure same number of original and simulated config files
#######################################
function validate_files {
    if [ "${#config_files[@]}" -ne "${#iface_files[@]}" ]; then
        signal_fail 1 "Simulated interface files not same number as original config files"
    else
        printf "${GREEN}Validated same number of config files and simulated logs${NC}\n"
    fi
}

##############################################################################
######################## PARSING DATA SECTION ################################
##############################################################################

#######################################
# Parse original interfaces taken from the device configs
#######################################
function parse_device_configs {
    rm -f ${IFACES_ORIG_FILE}

    for f in "${config_files[@]}"
    do
        local filename=$(echo ${f##*/})
        filename=$(echo ${filename%.*})

        grep -E '(^interface|ip address)' ${f} | sed '$!N;s/\n/,/' \
        | awk '{print $2 $5}' | sed -e "s/^/$filename,/" >> ${IFACES_ORIG_FILE}
        signal_fail $? "Processing ${f}"
    done

    printf "${GREEN}Parsed original device configurations to a csv file${NC}\n"
}

#######################################
# Parse simulated interfaces data from Layer 3
#######################################
function parse_iface_logs {
    rm -f ${IFACES_SIM_FILE}

    for f in "${iface_files[@]}"
    do
        local filename=$(echo ${f##*_})
        filename=$(echo ${filename%.*})
        # pair every two lines
        sed '$!N;s/\n/,/' ${f} | sed '/10.0./!d' \
        | sed -e "s/^/${filename},/" >> ${IFACES_SIM_FILE}
        signal_fail $? "Processing ${f}"
    done

    printf "${GREEN}Parsed simulated device configurations to a csv file${NC}\n"
}

##############################################################################
######################## MATCHING DATA SECTION ###############################
##############################################################################

#######################################
# Invoke python script to perform subnet matching and all
# Output: /nat_files/matched-*.csv
#######################################
function py_perform_matching {
    python NatController.py -t ${FLAG_topology}
}

##############################################################################
######################## PERFORMING SED SECTION ##############################
##############################################################################
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
# Auxiliary function for sed-ing files device by device
#######################################
function sed_aux {
    local matched_file=$1

    for f in "${config_files[@]}"
    do
        local filename=$(echo ${f##*/})
        filename=$(echo ${filename%.*})

        while IFS=, read -r dev old new
        do
            if [[ ${dev} == ${filename} ]]; then
                sed -i -e "s%${old}%${new}%g" ${f}
                signal_fail $? "Sed-ing ${f}"
            fi
        done < "${matched_file}"
        printf "${GREEN}Translated ${filename} ${NC}\n"
    done
}

function sed_ifaces {
    sed_aux "${MATCHED_IFACES}"
}

function sed_ips {
    sed_aux "${MATCHED_IPS}"
}

##############################################################################
######################### ACTUAL SCRIPT LOGIC ################################
##############################################################################
###### Performing NAT ######${NC}\n"
printf "${CYAN}#### Reading files ####${NC}\n"
copy_config_files
read_config_files
read_iface_log_files
validate_files

printf "${CYAN}#### Parsing logs ####${NC}\n"
mkdir -p ${DPL_NAT_DIR}
parse_device_configs
parse_iface_logs

printf "${CYAN}#### Performing network matching (python) ####${NC}\n"
py_perform_matching

printf "${CYAN}#### Performing NAT ####"
echo "## Updating subnets ##"
sed_subnets
echo "## Updating interfaces ##"
sed_ifaces
echo "## Updating IP addresses ##"
sed_ips
