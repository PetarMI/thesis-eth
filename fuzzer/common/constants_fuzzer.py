import os

# top-level dirs
HOME_LOC = os.environ['HOME']
FUZZ_DIR = "{}/thesis-eth/fuzzer".format(HOME_LOC)

FUZZ_DATA_DIR = "{}/fuzz_data".format(FUZZ_DIR)
CONTROLLER_DATA_DIR = "{}/controller_data".format(FUZZ_DATA_DIR)
EXECUTOR_DATA_DIR = "{}/executor_data".format(FUZZ_DATA_DIR)
VERIFIER_DATA_DIR = "{}/verifier_data".format(FUZZ_DATA_DIR)

# running topology data files
PROPERTIES_FILE = "{}/properties.json".format(CONTROLLER_DATA_DIR)
TOPO_FILE = "{}/topo.json".format(CONTROLLER_DATA_DIR)
IP_NAT_FILE = "{}/nat_ips.csv".format(CONTROLLER_DATA_DIR)
VM_FILE = "{}/running_vms.conf".format(CONTROLLER_DATA_DIR)

# files used for fuzzing
PARSED_PROPS_FILE = "{}/reachability_props.json".format(VERIFIER_DATA_DIR)
REACH_PROPS_FILE = "{}/reachability_instr.csv".format(EXECUTOR_DATA_DIR)
