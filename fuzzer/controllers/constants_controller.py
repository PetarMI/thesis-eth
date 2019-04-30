import os

# top-level dirs
HOME_LOC = os.environ['HOME']
WORK_DIR = "{}/thesis-eth".format(HOME_LOC)
FUZZ_DIR = "{}/fuzzer".format(WORK_DIR)
FUZZ_DATA_DIR = "{}/fuzz_data".format(FUZZ_DIR)
INPUT_DATA_DIR = "{}/controller_data".format(FUZZ_DATA_DIR)
OUTPUT_DATA_DIR = "{}/executor_data".format(FUZZ_DATA_DIR)

# running topology data files
PROPERTIES_FILE = "{}/properties.json".format(INPUT_DATA_DIR)
TOPO_FILE = "{}/topo.json".format(INPUT_DATA_DIR)
IP_NAT_FILE = "{}/nat_ips.csv".format(INPUT_DATA_DIR)
VM_FILE = "{}/running_vms.conf".format(INPUT_DATA_DIR)

# files used for fuzzing
REACH_FILE = "{}/reachability_props.csv".format(OUTPUT_DATA_DIR)
