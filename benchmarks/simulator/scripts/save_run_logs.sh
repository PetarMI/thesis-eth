ARG_topo="$1"
ARG_run="$2"

# VM paths
readonly VM_LOG="/logs/setup.log"

# Local paths
readonly HOME_DIR="$HOME"
readonly BENCH_DIR="${HOME_DIR}/thesis-eth/benchmarks/simulator/depl_files"
readonly RUN_DIR="${BENCH_DIR}/${ARG_topo}/run_${ARG_run}"

# VM connect info
readonly CONF_FILE="${HOME}/thesis-eth/infra/deployer/vm_comms/running_vms.conf"
readonly USER="fuzzvm"

function download_setup_logs {
    while IFS=, read -r idx vm_id role
    do
        echo "#### Downloading from VM ${idx} ####"
        scp "${USER}@${vm_id}:.${VM_LOG}" "${RUN_DIR}/setup_${idx}.log" 1>/dev/null
    done < ${CONF_FILE}
}

mkdir -p ${RUN_DIR}
download_setup_logs

