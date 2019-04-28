import os

# top-level dirs
HOME_LOC = os.environ['HOME']
WORK_DIR = "{}/thesis-eth".format(HOME_LOC)
FUZZ_DIR = "{}/fuzzer".format(WORK_DIR)
DATA_DIR = "{}/run_data".format(FUZZ_DIR)

PROPERTIES_FILE = "{}/properties.json".format(DATA_DIR)
TOPO_FILE = "{}/topo.json".format(DATA_DIR)
IP_NAT_FILE = "{}/nat_ips.csv".format(DATA_DIR)
VM_FILE = "{}/running_vms.conf".format(DATA_DIR)