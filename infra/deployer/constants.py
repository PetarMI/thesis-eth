# project dir
WORK_DIR = "/home/pesho/D/thesis-repo"
TOPO_DIR = "{}/topologies".format(WORK_DIR)
DEPLOYER_DIR = "{}/infra/deployer".format(WORK_DIR)

# subdirectories
DPL_FILES_DIR = "{}/deployment_files".format(DEPLOYER_DIR)

# Compose constants
COMPOSE_DIR = "/compose_files"

NET_COMPOSE_FILE = "net-compose.csv"
CONTAINER_COMPOSE_FILE = "containers.csv"
LINKS_COMPOSE_FILE = "links.csv"

VM_NAME = "netvm"

# NAT constants
LOGS_DIR = "/net_logs"
NAT_FILES = "/nat_files"

NET_LOG_FILE = "networks.log"

SUBNETS_FILE = "matched-subnets.csv"
IFACES_FILE = "matched-ifaces.csv"
IPS_FILE = "matched-ips.csv"
ORIG_IFACES_FILE = "orig_ifaces.csv"
SIM_IFACES_FILE = "sim_ifaces.csv"
