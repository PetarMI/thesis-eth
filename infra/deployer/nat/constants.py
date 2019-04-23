import os

# top-level dirs
HOME_LOC = os.environ['HOME']
WORK_DIR = "{}/thesis-eth".format(HOME_LOC)
TOPO_DIR = "{}/topologies".format(WORK_DIR)
DEPLOYER_DIR = "{}/infra/deployer".format(WORK_DIR)

# subdirectories
DPL_FILES_DIR = "{}/deployment_files".format(DEPLOYER_DIR)

# NAT constants
LOGS_DIR = "/net_logs"
NAT_FILES = "/nat_files"

NET_LOG_FILE = "networks.log"

SUBNETS_FILE = "matched-subnets.csv"
IFACES_FILE = "matched-ifaces.csv"
IPS_FILE = "matched-ips.csv"
ORIG_IFACES_FILE = "orig_ifaces.csv"
SIM_IFACES_FILE = "sim_ifaces.csv"
