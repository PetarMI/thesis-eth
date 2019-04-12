import ipaddress
from typing import Tuple
import file_reader as fr


def perform_match(topo_name: str, matched_subnets: dict) -> Tuple[dict, dict]:
    orig_ifaces: dict = fr.read_orig_ifaces(topo_name)
    sim_ifaces: dict = fr.read_sim_ifaces(topo_name)

    validate_input(orig_ifaces, sim_ifaces)

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
    """ Find the simulated IP and iface of a device

    :param sim_subnet: simulated subnet we care about
    :param sim_config: all simulated pairs of IPs and iface for that device
    :return: simulated IP and iface for that subnet
    """
    for sim_iface, sim_ip in sim_config.items():
        if (ipaddress.IPv4Network(sim_subnet) == ipaddress.IPv4Interface(sim_ip).network):
            return sim_iface, sim_ip


def validate_input(o_ifaces: dict, s_ifaces: dict):
    # validate IPs
    if not check_same_devices(o_ifaces, s_ifaces):
        raise KeyError("Different devices")

    if not check_same_length(o_ifaces, s_ifaces):
        raise KeyError("Different interfaces")


# @Tested
def check_same_devices(o_ifaces: dict, s_ifaces: dict) -> bool:
    return set(o_ifaces.keys()) == set(s_ifaces.keys())


def check_same_length(o_ifaces: dict, s_ifaces: dict) -> bool:
    for dev, o_configs in o_ifaces.items():
        num_o_ifaces = len(o_configs)
        num_s_ifaces = len(s_ifaces[dev])

        if num_o_ifaces != num_s_ifaces:
            return False

    return True
