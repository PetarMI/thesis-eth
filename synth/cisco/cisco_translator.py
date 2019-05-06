from argparse import ArgumentParser
from synth.common import file_reader as fr
from synth.cisco import links_parser as lp
from synth.cisco import config_parser as cp
from synth.cisco import topo_merger as tm
from synth.cisco import topo_generator as tg
from synth.cisco import config_generator as cg
import json


def parse_topology(topo_name: str):
    # Parse the links file
    raw_links: dict = fr.read_raw_links(topo_name)
    links: dict = lp.parse_links(raw_links)

    # Parse Cisco configs
    hosts = links.keys()
    cisco_configs: dict = fr.read_cisco_configs(topo_name, hosts)
    configs = cp.parse_configs(cisco_configs)

    # Generate the topo file and configs
    topo_configs: dict = tm.merge_topo_data(links, configs)
    tg.generate_topo(topo_configs, topo_name)
    cg.generate_config_files(configs, topo_name)
    # print(json.dumps(links, indent=4))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topo", dest="topo",
                        help="Name of the cisco topology")
    args = parser.parse_args()

    parse_topology(args.topo)
