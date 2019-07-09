import os

HOME_LOC = os.environ['HOME']
LOG_DIR = "{}/thesis-eth/benchmarks/fuzzer/logs".format(HOME_LOC)

REVERT_STATS = "{}/depl_stats.log".format(LOG_DIR)
