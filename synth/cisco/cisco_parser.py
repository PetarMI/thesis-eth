from argparse import ArgumentParser
from synth.common import file_reader as fr
from synth.cisco import links_parser as lp
from synth.cisco import config_parser as cp
from synth.cisco import topo_merger as tm
import json


def parse_topology(topo_name: str):
    """ Topo-level function to read input and call main parsing functions """
    raw_links: dict = fr.read_raw_links(topo_name)
    links: dict = lp.parse_links(raw_links)
    # print(json.dumps(raw_links, indent=4))

    hosts = links.keys()
    cisco_configs: dict = fr.read_cisco_configs(topo_name, hosts)
    configs = cp.parse_configs(cisco_configs)
    # print(json.dumps(configs, indent=4))

    topo_configs: dict = tm.merge_topo_data(links, configs)
    #print(json.dumps(topo_configs, indent=4))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topo", dest="topo",
                        help="Name of the cisco topology")
    args = parser.parse_args()

    parse_topology(args.topo)