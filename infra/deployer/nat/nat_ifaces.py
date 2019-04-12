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


# @Tested
def find_sim_subnet(o_ip: str, matched_subnets: dict) -> str:
    orig_subnet = str(ipaddress.IPv4Interface(o_ip).network)

    sim_subnet = matched_subnets.get(orig_subnet, None)

    if sim_subnet is None:
        raise ValueError("No sim subnet match")

    return sim_subnet


# @Tested
def find_sim_config(sim_subnet: str, sim_config: dict) -> Tuple[str, str]:
    """ Find the simulated IP and iface of a device

    :param sim_subnet: simulated subnet we care about
    :param sim_config: all simulated pairs of IPs and iface for that device
    :return: simulated IP and iface for that subnet
    """
    matches = 0
    sim_iface = None
    sim_ip = None

    for s_iface, s_ip in sim_config.items():
        if (ipaddress.IPv4Network(sim_subnet) == ipaddress.IPv4Interface(s_ip).network):
            sim_iface = s_iface
            sim_ip = s_ip
            matches += 1

    if matches == 0:
        raise ValueError("No sim IP match")
    elif matches > 1:
        # technically impossible to go here cause of check_repeated_subnets
        raise ValueError("Multiple sim IP match")
    else:
        return sim_iface, sim_ip


# #############################################################################
# ########################## VALIDATION #######################################
# #############################################################################
def validate_input(o_ifaces: dict, s_ifaces: dict):
    # TODO validate IPs

    if not check_same_devices(o_ifaces, s_ifaces):
        raise KeyError("Different devices")

    if not check_same_length(o_ifaces, s_ifaces):
        raise KeyError("Different interfaces")

    check_repeated_subnets(o_ifaces)
    check_repeated_subnets(s_ifaces)


# @Tested
def check_same_devices(o_ifaces: dict, s_ifaces: dict) -> bool:
    if len(o_ifaces.keys()) == 0:
        raise KeyError("No devices in orig file")

    if len(s_ifaces.keys()) == 0:
        raise KeyError("No devices in sim file")

    return set(o_ifaces.keys()) == set(s_ifaces.keys())


# @Tested
def check_same_length(o_ifaces: dict, s_ifaces: dict) -> bool:
    for dev, o_configs in o_ifaces.items():
        num_o_ifaces = len(o_configs)
        num_s_ifaces = len(s_ifaces[dev])

        if num_o_ifaces == 0 or num_s_ifaces == 0:
            raise KeyError("No interfaces on device {}".format(dev))

        if num_o_ifaces != num_s_ifaces:
            return False

    return True


# @Tested
def check_repeated_subnets(configs: dict):
    for dev, conf in configs.items():
        subnets = []
        for ipaddr in conf.values():
            subnet = str(ipaddress.IPv4Interface(ipaddr).network)
            if subnet in subnets:
                raise ValueError("Repeated subnets in device {}".format(dev))
            else:
                subnets.append(subnet)

    return True
