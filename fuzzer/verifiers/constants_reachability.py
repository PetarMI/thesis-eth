import os

# top-level dirs
HOME_LOC = os.environ['HOME']
FUZZ_DIR = "{}/thesis-eth/fuzzer".format(HOME_LOC)
PING_LOGS_DIR = "{}/fuzz_data/verifier_data/ping_logs".format(FUZZ_DIR)
