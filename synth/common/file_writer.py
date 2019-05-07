import json
import os
from synth.common import constants_synth as const


def write_topo_file(topo_name: str, topo_data: dict):
    topo_dir= "{}/{}".format(const.GEN_DIR, topo_name)
    os.makedirs(topo_dir, exist_ok=True)

    topo_file = "{}/{}.topo".format(topo_dir, topo_name)

    with open(topo_file, 'w+') as json_outfile:
        json.dump(topo_data, json_outfile, indent=4)


def write_config_files(topo_name: str, frr_configs: dict):
    topo_dir = "{}/{}".format(const.GEN_DIR, topo_name)
    config_dir = const.CONFIG_DIR.format(topo_dir)
    os.makedirs(config_dir, exist_ok=True)

    for hostname, host_configs in frr_configs.items():
        filename = "{}-{}.conf".format(topo_name, hostname.lower())
        config_file = "{}/{}".format(config_dir, filename)

        with open(config_file, 'w+') as conf_file:
            for instr in host_configs:
                conf_file.write("{}\n".format(instr))
