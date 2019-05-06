import json
import os
from synth.common import constants_synth as const


def write_topo_file(topo_name: str, topo_data: dict):
    topo_dir= "{0}/{1}".format(const.GEN_DIR, topo_name)
    os.makedirs(topo_dir, exist_ok=True)

    topo_file = "{}/{}.topo".format(topo_dir, topo_name)

    with open(topo_file, 'w+') as json_outfile:
        json.dump(topo_data, json_outfile, indent=4)
