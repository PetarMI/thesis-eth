from argparse import ArgumentParser
from synth.common import file_reader as fr
from synth.common import constants_synth as const
import json


def parse_topology(topo_name: str):
    raw_links: dict = fr.read_raw_links(topo_name)
    links: dict = parse_links(raw_links)

    hosts = links.keys()
    cisco_configs: dict = fr.read_cisco_configs(topo_name, hosts)
    configs = parse_configs(cisco_configs)

    #print(json.dumps(links, indent=4, sort_keys=True))


def parse_links(raw_links: dict) -> dict:
    validate_links(raw_links)
    links: dict = assign_sim_nets(raw_links)

    return links


def parse_configs(cisco_configs: dict) -> dict:
    for hostname, host_config in cisco_configs.items():
        parsed_config: dict = parse_host(host_config)


def assign_sim_nets(raw_links) -> dict:
    """ Create simulated networks and assign each link to one """
    links = dict()

    for host, host_links in raw_links.items():
        links.setdefault(host, {})
        for endpoint in host_links:
            sim_net = get_sim_net(host, endpoint, links)
            links[host].update({endpoint: sim_net})

    return links


def get_sim_net(host: str, endpoint: str, links: dict) -> str:
    if links.get(endpoint, None):
        sim_net: str = links[endpoint][host]
    else:
        sim_net: str = get_net_name(host, endpoint)

    return sim_net


def parse_host(host_cisco_config: str) -> dict:
    return dict()


def get_net_name(host: str, endpoint: str) -> str:
    return "net-{}-{}".format(host.lower(), endpoint.lower())


def validate_links(raw_links: dict):
    """ Ensure hosts have a duplex link in links file """
    for host, host_links in raw_links.items():
        for endpoint in host_links:
            if not raw_links.get(endpoint, None):
                raise ValueError("Missing top-level entry for host {}".format(endpoint))

            if host not in raw_links[endpoint]:
                raise ValueError("No duplex link between {} and {}".format(host, endpoint))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topo", dest="topo",
                        help="Name of the cisco topology")
    args = parser.parse_args()

    parse_topology(args.topo)
