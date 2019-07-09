import os

HOME_LOC = os.environ['HOME']
LOG_DIR = "{}/thesis-eth/benchmarks/simulator/logs".format(HOME_LOC)

TOPO_LOG_DIR = "{}/depl_times".format(LOG_DIR)
VM_LOGS_DIR = "{}/optimal_vms".format(LOG_DIR)

VM_LOGS = "vm_{}"
RUN_LOGS = "run_{}"

RUNS = 3

DEPL_STATS = "depl_stats.log"
SETUP = "setup_{}.log"
