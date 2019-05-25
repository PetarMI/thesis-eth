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
def find_container_vm(container: str, containers: dict, vms: dict) -> str:
    """ Returns the IP address of the VM running the specified container """
    container_info = containers.get(container, None)

    if container_info is None:
        raise ValueError("Property src container {} not in topo file".format(container))

    vm_id = container_info["vm"]
    vm = vms.get(vm_id, None)

    if vm is None:
        raise ValueError("No running VM with ID {}".format(vm_id))

    return vm["ip"]


# @Tested
def find_network_devices(network: str, net2dev: dict) -> list:
    net_devices: list = net2dev.get(network, None)

    if net_devices is None:
        raise ValueError("Network {} does not exist in fuzzing data logs".format(network))

    return net_devices


def get_nat_ip(dest_ip: str, nat_ips: dict) -> str:
    """ Check every container for the original IP and return the simulated one.
    Works with dest_ip which has no netmask specified
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
