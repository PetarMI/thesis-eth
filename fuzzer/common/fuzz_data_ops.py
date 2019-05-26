""" Fuzzing data operations

This script collects all operations for finding something in the
fuzzing data, i.e. data of the running containers.

How to use: All functions are implemented to work on the data format
            stored in the fuzzer.common.FuzzData class
"""

import ipaddress


def get_network_names(topo_networks: list) -> list:
    """ Get a list of all network names """
    nets = []

    for net in topo_networks:
        nets.append(net["name"])

    return nets


# @Tested
def find_container_vm(container: str, dev2vm: dict) -> str:
    """ Returns the IP address of the VM running the specified container """
    vm_ip: str = dev2vm.get(container, None)

    if not vm_ip:
        raise ValueError("Container {} does not exist in dev2vm logs".format(container))

    return vm_ip


# @Tested
def find_network_devices(network: str, net2dev: dict) -> list:
    """ Find the devices attached to the specified network """
    net_devices: list = net2dev.get(network, None)

    if net_devices is None:
        raise ValueError("Network {} does not exist in net2dev logs".format(network))

    return net_devices


def get_nat_ip(dest_ip: str, nat_ips: dict) -> str:
    """ Check every container for the original IP and return the simulated one.
    Works with dest_ip which has no netmask specified
    Called just once during property parsing.
    """
    casted_dest_ip = ipaddress.IPv4Address(dest_ip)

    for container in nat_ips.values():
        for orig_iface in container.keys():
            casted_orig_ip = orig_iface.ip

            if casted_dest_ip == casted_orig_ip:
                sim_dest_ip = container[orig_iface]
                return str(sim_dest_ip.ip)

    # raise ValueError("Original IP {} not in NAT logs".format(dest_ip))
    print("WARNING: Original IP {} not in NAT logs".format(dest_ip))
    return dest_ip
