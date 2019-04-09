# project dir
WORK_DIR = "/home/pesho/D/thesis-repo"
TOPO_DIR = "{}/topologies".format(WORK_DIR)
DEPLOYER_DIR = "{}/infra/deployer".format(WORK_DIR)

# subdirectories
DPL_FILES_DIR = "{}/deployment_files".format(DEPLOYER_DIR)

# leaf directories
COMPOSE_DIR = "/compose_files"
LOGS_DIR = "/net_logs"
NAT_FILES = "/nat_files"

# filenames
NET_FILE = "net-compose.csv"
SUBNETS_FILE = "matched-subnets.csv"
CONTAINER_FILE = "containers"
LINKS_FILE = "links"
NET_LOG_FILE = "networks.log"

# other
VM_NAME = "netvm"
FILE_EXT = ".csv"
