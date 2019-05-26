""" Fuzzing data collection

The purpose of this class is to be a wrapper around all fuzzing data.
All info which will be frequently accessed is kept in memory and
restructured via the static methods so that they have a primary key that
allows quick search. Other data is simply read from file as if the caller
uses the file_reader.

How to use: Other modules should import just the class via
            from fuzzer.common.FuzzData import FuzzData
"""

import ipaddress
from fuzzer.common import file_reader as fr


class FuzzData:
    def __init__(self):
        topo: dict = fr.read_topo()
        topo_containers: list = topo["containers"]
        sim_nets: dict = fr.read_sim_networks()
        sim_ifaces: dict = fr.read_sim_ifaces()
        vms: dict = fr.read_vm_info()

        self.dev2vm: dict = parse_dev2vm(topo_containers, vms)
        self.net2dev: dict = parse_net2devices(topo["meta"]["name"], topo_containers)
        self.dev_ifaces2net = parse_nets2ifaces(topo_containers, sim_ifaces, sim_nets)

    # in-memory data
    def get_dev2vm(self) -> dict:
        return self.dev2vm

    def get_net2dev(self) -> dict:
        return self.net2dev

    def get_dev_ifaces2net(self) -> dict:
        return self.dev_ifaces2net

    # TODO: check which of these are needed
    # wrapper methods
    def get_topo_name(self) -> dict:
        topo: dict = fr.read_topo()
        return topo["meta"]["name"]

    def get_topo_networks(self) -> list:
        topo: dict = fr.read_topo()
        return topo["networks"]

    def get_vms(self):
        return fr.read_vm_info()

    def get_nat_ips(self):
        return fr.read_nat_ips()


# @Tested
def parse_dev2vm(topo_containers: list, vms: dict) -> dict:
    dev2vm = dict()

    for container in topo_containers:
        container_vm = vms.get(container["vm"], None)
        check_none(container_vm, "No running vm with id {}".format(container["vm"]))

        dev2vm.update({container["name"]: container_vm["ip"]})

    return dev2vm


# @Tested
def parse_net2devices(topo_name: str, topo_containers: list) -> dict:
    """ Return a dict of network names to connected devices so that we
        have the network name as a primary key.
    """
    net2dev = dict()

    for container in topo_containers:
        for iface in container["interfaces"]:
            net: str = prepend_topo(topo_name, iface["network"])
            topo_container: str = prepend_topo(topo_name, container["name"])

            net2dev.setdefault(net, []).append(topo_container)

    net2dev_post_validation(net2dev)

    return net2dev


# TODO fix naming
# @Tested (just one)
def parse_nets2ifaces(topo_containers: list, sim_nets: dict, sim_ifaces: dict) -> dict:
    """ Parse the containers and match each interface to a network """
    dev_ifaces2nets = dict()

    for container in topo_containers:
        container_sim_ifaces = sim_ifaces.get(container["name"], None)
        check_none(container_sim_ifaces, "Container {} not found in sim ifaces file".format(container["name"]))

        nets2ifaces: dict = match_dev_net2iface(container_sim_ifaces, sim_nets)

        dev_ifaces2nets.update({container["name"]: nets2ifaces})

    return dev_ifaces2nets


# @Tested
def match_dev_net2iface(dev_sim_ifaces: dict, sim_nets: dict) -> dict:
    matched_ifaces = dict()

    for iface_ip, iface_name in dev_sim_ifaces.items():
        iface_net_ip = str(ipaddress.IPv4Interface(iface_ip).network)
        iface_network = sim_nets.get(iface_net_ip, None)
        check_none(iface_network, "Network {} does not exist".format(iface_net_ip))

        matched_ifaces.update({iface_network: iface_name})

    return matched_ifaces


# @Tested as part of calling function
def net2dev_post_validation(net2dev: dict):
    """ Verify that a link has at most two connected devices """
    for net, containers in net2dev.items():
        if len(containers) > 2:
            raise ValueError("More than two containers connected to network {}"
                             .format(net))


# def iface2net_post_validation(container_ifaces: list, nets2ifaces: dict):
#     if len(container_ifaces) != len(nets2ifaces.keys()):
#         raise ValueError("Bad: Inconsistent container interfaces length")
#
#     for iface in container_ifaces:
#         if iface["name"] not in nets2ifaces.keys():
#             raise ValueError("Bad: Inconsistent container interfaces")


# @Tested
def check_none(item, msg: str):
    if not item:
        raise ValueError(msg)


def prepend_topo(topo_name: str, entity: str) -> str:
    return "{}-{}".format(topo_name, entity)
