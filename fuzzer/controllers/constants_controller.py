import os

# top-level dirs
HOME_LOC = os.environ['HOME']
WORK_DIR = "{}/thesis-eth".format(HOME_LOC)
FUZZ_DIR = "{}/fuzzer".format(WORK_DIR)
RUN_DATA_DIR = "{}/run_data".format(FUZZ_DIR)
FUZZ_DATA_DIR = "{}/fuzz_data".format(FUZZ_DIR)

# running topology data files
PROPERTIES_FILE = "{}/properties.json".format(RUN_DATA_DIR)
TOPO_FILE = "{}/topo.json".format(RUN_DATA_DIR)
IP_NAT_FILE = "{}/nat_ips.csv".format(RUN_DATA_DIR)
VM_FILE = "{}/running_vms.conf".format(RUN_DATA_DIR)

# files used for fuzzing
REACH_FILE = "{}/reachability_props.csv".format(FUZZ_DATA_DIR)
