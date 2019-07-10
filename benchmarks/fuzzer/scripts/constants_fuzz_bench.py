import os

HOME_LOC = os.environ['HOME']
LOG_DIR = "{}/thesis-eth/benchmarks/fuzzer/logs".format(HOME_LOC)
TOPO_DIR = "{}/thesis-eth/topologies".format(HOME_LOC)
GEN_DIR = "{}/thesis-eth/benchmarks/fuzzer/generated".format(HOME_LOC)

PROPERTIES_FILE = "{}_properties.json"
PRETTY_PROPERTIES_FILE = "{}_pretty_properties.txt"
REVERT_STATS = "{}/depl_stats.log".format(LOG_DIR)
