import os

HOME_LOC = os.environ['HOME']
FUZZER_DIR = "{}/thesis-eth/benchmarks/fuzzer".format(HOME_LOC)

LOG_DIR = "{}/logs".format(FUZZER_DIR)
GEN_DIR = "{}/generated".format(FUZZER_DIR)
TOPO_DIR = "{}/thesis-eth/topologies".format(HOME_LOC)

VIOLATIONS_DIR = "{}/violations_measurements".format(LOG_DIR)

PROPERTIES_FILE = "{}_properties.json"
PRETTY_PROPERTIES_FILE = "{}_pretty_properties.txt"
REVERT_STATS = "{}/link_ops.log".format(LOG_DIR)
