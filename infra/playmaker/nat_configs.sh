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
readonly DEPLOY_DIR="${WORK_DIR}/infra/playmaker/deployment_files/${FLAG_topology}"
readonly DPL_CONFIG_DIR="${DEPLOY_DIR}/device_configs"

# files
readonly SUBNETS_FILE="${DEPLOY_DIR}/nat_files/matched-subnets.csv"

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
            updated_file=$(sed -i -e "s%${old}%${new}%g" ${f})
        done < "${SUBNETS_FILE}"
    done
}

#######################################
# Actual script logic
#######################################
#copy_files
read_filenames
sed_subnets


