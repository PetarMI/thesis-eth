""" Fuzzing data operations

This script collects all operations for finding something in the
fuzzing data, i.e. data of the running containers.

How to use: All functions are implemented to work on the data format
            stored in the fuzzer.common.FuzzData class
"""

import ipaddress


# @Tested
def find_container_vm(container: str, dev2vm: dict) -> str:
    """ Returns the IP address of the VM running the specified container """
    vm_ip: str = dev2vm.get(container, None)
    check_none(vm_ip, "Container {} does not exist in dev2vm logs"
               .format(container))

    return vm_ip


# @Tested
def find_network_devices(network: str, net2dev: dict) -> list:
    """ Find the devices attached to the specified network """
    net_devices: list = net2dev.get(network, None)
    check_none(net_devices, "Network {} does not exist in net2dev logs"
               .format(network))

    return net_devices


# @Tested
def find_network_interface(container: str, network: str, dev_net2iface) -> str:
    """ Find the interface through which a device is connected to a
        specific network.
    """
    container_networks: dict = dev_net2iface.get(container, None)
    check_none(container_networks, "Problem with container {} in dev_net2iface logs"
               .format(container))

    network_interface: str = container_networks.get(network, None)
    check_none(network_interface, "Problem with network {} on container {} in dev_net2iface logs"
               .format(network, container))

    return network_interface


# @Tested
def find_ip_dev(ip: str, ip2dev: dict) -> str:
    """ Return the device to which has the specified IP """
    return ip2dev.get(ip, None)


def get_nat_iface(dest_ip: str, nat_ips: dict) -> ipaddress.IPv4Interface:
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
                return sim_dest_ip

    raise ValueError("Original IP {} not in NAT logs".format(dest_ip))
    # print("WARNING: Original IP {} not in NAT logs".format(dest_ip))
    # return dest_ip


# @Tested in FuzzData.py tests
def check_none(item, msg: str):
    if not item:
        raise ValueError(msg)
