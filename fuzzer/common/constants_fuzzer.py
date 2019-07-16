import os

# top-level dirs
HOME_LOC = os.environ['HOME']
FUZZ_DIR = "{}/thesis-eth/fuzzer".format(HOME_LOC)

FUZZ_DATA_DIR = "{}/fuzz_data".format(FUZZ_DIR)
CONTROLLER_DATA_DIR = "{}/controller_data".format(FUZZ_DATA_DIR)
EXECUTOR_DATA_DIR = "{}/executor_data".format(FUZZ_DATA_DIR)
VERIFIER_DATA_DIR = "{}/verifier_data".format(FUZZ_DATA_DIR)

PING_LOGS_DIR = "{}/ping_logs".format(VERIFIER_DATA_DIR)

# running topology data files
PROPERTIES_FILE = "{}/properties.json".format(CONTROLLER_DATA_DIR)
TOPO_FILE = "{}/topo.json".format(CONTROLLER_DATA_DIR)
IP_NAT_FILE = "{}/nat_ips.csv".format(CONTROLLER_DATA_DIR)
VM_FILE = "{}/running_vms.conf".format(CONTROLLER_DATA_DIR)
NETS_FILE = "{}/networks.csv".format(CONTROLLER_DATA_DIR)
SIM_IFACES_FILE = "{}/sim_ifaces.csv".format(CONTROLLER_DATA_DIR)

# files used for fuzzing
PARSED_PROPS_FILE = "{}/reachability_props.json".format(VERIFIER_DATA_DIR)
PARSED_ISO_FILE = "{}/isolation_props.json".format(VERIFIER_DATA_DIR)
REACH_PROPS_FILE = "{}/reachability_instr.csv".format(EXECUTOR_DATA_DIR)

PING_FILE = "ping_res_{}.log"
FAILURES_LOG = "{}/failures.log".format(VERIFIER_DATA_DIR)

# Executor scripts
CONVERGENCE_SH = "{}/executors/convergence_monitor.sh".format(FUZZ_DIR)
LINK_STATE_SH = "{}/executors/exec_link_change.sh".format(FUZZ_DIR)
PING_SH = "{}/executors/ping_reachability.sh".format(FUZZ_DIR)
FIB_SH = "{}/executors/fib_reachability.sh".format(FUZZ_DIR)
FIB_NEXT_HOP_SH = "{}/executors/fib_next_hops.sh".format(FUZZ_DIR)
VM_STATE_SH = "{}/executors/vm_save_state.sh".format(FUZZ_DIR)
FIB_INFO_SH = "{}/executors/get_fib.sh".format(FUZZ_DIR)

RESTORE = "restore"
DROP = "drop"

REACH_FUZZ = "reachability"
ISO_FUZZ = "isolation"

CONV_TIME = 15
