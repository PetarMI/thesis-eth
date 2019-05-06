import os

HOME_DIR = os.environ['HOME']
SYNTH_DIR = "{}/thesis-eth/synth".format(HOME_DIR)
GEN_DIR = "{}/gen".format(SYNTH_DIR)
CISCO_DIR = "{}/cisco/cisco_configs".format(SYNTH_DIR)

CONFIG_DIR = "{}/device_configs"
LINKS_FILE = "links.txt"

# FRR commands
CMD_FRR_VER = "frr version 6.0.2"
CMD_FRR_DEF = "frr defaults traditional"
CMD_HOST = "hostname {}"
CMD_INTEGRATED = "service integrated-vtysh-config"
CMD_END_SEC = "!"
