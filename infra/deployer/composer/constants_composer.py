import os

# top-level dirs
HOME_LOC = os.environ['HOME']
WORK_DIR = "{}/D/thesis-repo".format(HOME_LOC)
TOPO_DIR = "{}/topologies".format(WORK_DIR)
DEPLOYER_DIR = "{}/infra/deployer".format(WORK_DIR)

# subdirectories
DPL_FILES_DIR = "{}/deployment_files".format(DEPLOYER_DIR)

COMPOSE_DIR = "/compose_files"

NET_COMPOSE_FILE = "net-compose.csv"
CONTAINER_COMPOSE_FILE = "containers.csv"
LINKS_COMPOSE_FILE = "links.csv"

VM_NAME = "netvm"
