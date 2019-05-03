import os

HOME_DIR = os.environ['HOME']
SYNTH_DIR = "{}/thesis-eth/synth".format(HOME_DIR)
GEN_DIR = "{}/gen".format(SYNTH_DIR)
CISCO_DIR = "{}/cisco/cisco_configs".format(SYNTH_DIR)

CONFIGS_DIR = "{}/device_config"
LINKS_FILE = "links.txt"