#!/bin/bash

usage="Script to synthesize a sequence topology with arbitrary size

where:
    -n  Number of routers
    -h  Show this help text"

FLAG_size="youforgottopassatopologysize"

while getopts "n:h" option
do
    case "${option}" in
        n) FLAG_size=${OPTARG};;
        h) echo "${usage}"; exit;;
        *) echo "Unknown option"; exit 1;;
    esac
done

readonly WORK_DIR="$HOME"
readonly SEQ_DIR="${WORK_DIR}/thesis-eth/synth/gen/seq"
readonly CONFIG_DIR="${SEQ_DIR}/device_configs"
readonly CONFIG_FILE="${SEQ_DIR}/configs.csv"
readonly TEMPLATE_FILE="template.conf"

function signal_fail {
    local exit_code=$1
    local msg=$2
    if [[ ${exit_code} != 0 ]]; then
        echo "Failed with exit code ${exit_code}: ${msg}\n"
        exit ${exit_code}
    fi
}

function gen_topo {
    python seq_topo_gen.py -n ${FLAG_size}
}

function make_config_templates {
    rm -rf ${CONFIG_DIR}
    mkdir -p ${CONFIG_DIR}

    for i in $(seq 1 ${FLAG_size}); do
        cp ${TEMPLATE_FILE} "${CONFIG_DIR}/seq-r${i}.conf"
    done
}

function make_configs {
    while IFS=, read -r filename hostname rid s1 ip1 s2 ip2
    do
        sed -i -e "
        s%NEWHOSTNAME%${hostname}%g
        s%IPONE%${ip1}%g
        s%IPTWO%${ip2}%g
        s%ROUTERID%${rid}%g
        s%SUBNETONE%${s1}%g
        s%SUBNETTWO%${s2}%g
        " "${CONFIG_DIR}/${filename}"
        signal_fail $? "Sed-ing ${filename}"
    done < ${CONFIG_FILE}
}

gen_topo
make_config_templates
make_configs