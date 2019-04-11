import ipaddress
from typing import Tuple
import file_reader as fr


def perform_match(topo_name: str) -> Tuple[dict, dict]:
    orig_ifaces: dict = fr.read_orig_ifaces(topo_name)
    sim_ifaces: dict = fr.read_sim_ifaces(topo_name)
    matched_subnets: dict = fr.read_matched_subnets(topo_name)

    # this shouldn't really happen but check the return value anyway
    if (not make_sanity_checks(orig_ifaces, sim_ifaces)):
        exit(1)

    matched_ifaces, matched_ips = match(orig_ifaces, sim_ifaces, matched_subnets)

    return matched_ifaces, matched_ips


def match(orig_ifaces: dict, sim_ifaces: dict, matched_subnets: dict) -> Tuple[dict, dict]:
    matched_ifaces = {}
    matched_ips = {}

    for dev, orig_config in orig_ifaces.items():
        sim_config: dict = sim_ifaces.get(dev)
        dev_ifaces = {}
        dev_ips = {}

        for o_iface, o_ip in orig_config.items():
            sim_subnet = find_sim_subnet(o_ip, matched_subnets)
            sim_iface, sim_ip = find_sim_config(sim_subnet, sim_config)

            dev_ifaces.update({o_iface: sim_iface})
            dev_ips.update({o_ip: sim_ip})

        matched_ifaces.update({dev: dev_ifaces})
        matched_ips.update({dev: dev_ips})

    return matched_ifaces, matched_ips


def find_sim_subnet(o_ip: str, matched_subnets: dict) -> str:
    orig_subnet = str(ipaddress.IPv4Interface(o_ip).network)

    sim_subnet = matched_subnets.get(orig_subnet)
    return sim_subnet


def find_sim_config(sim_subnet: str, sim_config: dict) -> Tuple[str, str]:
    for sim_iface, sim_ip in sim_config.items():
        if (ipaddress.IPv4Network(sim_subnet) == ipaddress.IPv4Interface(sim_ip).network):
            return sim_iface, sim_ip


def make_sanity_checks(o_ifaces: dict, s_ifaces: dict) -> bool:
    return True
