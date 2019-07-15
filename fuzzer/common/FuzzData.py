""" Fuzzing data collection

The purpose of this class is to be a wrapper around all fuzzing data.
All info which will be frequently accessed is kept in memory and
restructured via the static methods so that they have a primary key that
allows quick search. Other data is simply read from file as if the caller
uses the file_reader.

How to use: Other modules should import just the class via
            from fuzzer.common.FuzzData import FuzzData

Convention:
    * Methods starting with `find_` are used repeatedly during fuzzing
    * Methods starting with `get_` are one-time operations

In-memory data: * dev2vm         - Container to VM IP
                * net2dev        - Network to attached containers
                * dev_net2ifaces - Container to networks to ifaces
"""

import ipaddress
from fuzzer.common import file_reader as fr
from fuzzer.common import fuzz_data_ops as fdata_ops


class FuzzData:
    def __init__(self):
        topo: dict = fr.read_topo()
        topo_containers: list = topo["containers"]
        topo_name = topo["meta"]["name"]
        inverted_sim_nets: dict = fr.read_sim_networks(swap=True)
        sim_ifaces: dict = fr.read_sim_ifaces()
        vms: dict = fr.read_vm_info()

        # parsed in-memory data for fuzzing
        self.dev2vm: dict = parse_dev2vm(topo_containers, vms, topo_name)
        self.net2dev: dict = parse_net2devices(topo_containers, topo_name)
        self.dev_net2iface = parse_nets2ifaces(sim_ifaces, inverted_sim_nets)
        self.ip2dev = parse_ip2dev(sim_ifaces)
        # read as-is in-memory data
        self.sim_nets: dict = fr.read_sim_networks()
        self.sim_nets_inverted: dict = fr.read_sim_networks(swap=True)

    # in-memory data operations
    def find_container_vm(self, container: str) -> str:
        return fdata_ops.find_container_vm(container, self.dev2vm)

    def find_network_devices(self, network: str) -> list:
        return fdata_ops.find_network_devices(network, self.net2dev)

    def find_network_interface(self, container: str, network: str) -> str:
        return fdata_ops.find_network_interface(container, network, self.dev_net2iface)

    def find_ip_device(self, ip: str) -> str:
        """
        :param ip: The IP address without mask
        :return: The name of the device which has this IP
        """
        return fdata_ops.find_ip_dev(ip, self.ip2dev)

    def get_ospf_networks(self) -> list:
        return fdata_ops.get_ospf_networks(self.net2dev)

    # wrapper methods
    def get_topo(self) -> dict:
        return fr.read_topo()

    def get_nat_ip(self, dest_ip: str):
        """ Return the simulated IP and the network it belongs to
            Used one-time for property parsing """
        nat_ips: dict = fr.read_nat_ips()
        nat_iface = fdata_ops.get_nat_iface(dest_ip, nat_ips)
        return str(nat_iface.ip), str(nat_iface.network)

    def get_link_nets(self, networks) -> list:
        """ Get the IPs of a list of network names """
        ips = []

        for net in networks:
            ips.append(self.get_sim_net_ip(net))

        return ips

    def get_sim_net_ip(self, net_name: str) -> str:
        net_ip: str = self.sim_nets.get(net_name, None)
        check_none(net_ip, "Network name does not exist in networks.log")
        return net_ip

    def get_sim_net_name(self, net_ip: str) -> str:
        net_name: str = self.sim_nets_inverted.get(net_ip, None)
        check_none(net_name, "Network IP does not exist in networks.log")
        return net_name

    def get_dev2vm(self) -> dict:
        return self.dev2vm


# @Tested
def parse_dev2vm(topo_containers: list, vms: dict, topo_name: str) -> dict:
    """ Return a dict of container names to IP of the VM they run on
        so that we have the container name as a primary key.
        """
    dev2vm = dict()

    for container in topo_containers:
        container_vm = vms.get(container["vm"], None)
        check_none(container_vm, "No running vm with id {}".format(container["vm"]))

        container_name: str = prepend_topo(topo_name, container["name"])
        dev2vm.update({container_name: container_vm["ip"]})

    return dev2vm


# @Tested
def parse_net2devices(topo_containers: list, topo_name: str) -> dict:
    """ Return a dict of network names to connected devices so that we
        have the network name as a primary key.
    """
    net2dev = dict()

    for container in topo_containers:
        for iface in container["interfaces"]:
            net: str = prepend_topo(topo_name, iface["network"])
            topo_container: str = prepend_topo(topo_name, container["name"])

            net2dev.setdefault(net, []).append(topo_container)

    post_validation_net2dev(net2dev)

    return net2dev


# @Tested
def parse_ip2dev(sim_ifaces: dict) -> dict:
    ip2dev = dict()

    for dev_name, dev_ifaces in sim_ifaces.items():
        for iface_ip in dev_ifaces.keys():
            ip = str(ipaddress.IPv4Interface(iface_ip).ip)
            ip2dev.update({ip: dev_name})

    post_validation_ip2dev(ip2dev, sim_ifaces)

    return ip2dev


# @Tested (just one)
def parse_nets2ifaces(sim_ifaces: dict, sim_nets: dict) -> dict:
    """ Parse the containers and match each interface to a network """
    dev_ifaces2nets = dict()

    for container, container_sim_ifaces in sim_ifaces.items():
        nets2ifaces: dict = match_dev_net2iface(container_sim_ifaces, sim_nets)

        dev_ifaces2nets.update({container: nets2ifaces})

    return dev_ifaces2nets


# @Tested
def match_dev_net2iface(dev_sim_ifaces: dict, sim_nets: dict) -> dict:
    """ Match a single container's interfaces to a network """
    matched_ifaces = dict()

    for iface_ip, iface_name in dev_sim_ifaces.items():
        iface_net_ip = str(ipaddress.IPv4Interface(iface_ip).network)
        iface_network = sim_nets.get(iface_net_ip, None)
        check_none(iface_network, "Network {} does not exist".format(iface_net_ip))

        matched_ifaces.update({iface_network: iface_name})

    return matched_ifaces


# @Tested as part of calling function
def post_validation_net2dev(net2dev: dict):
    """ Verify that a link has at most two connected devices """
    for net, containers in net2dev.items():
        if len(containers) > 2:
            raise ValueError("More than two containers connected to network {}"
                             .format(net))


# @Tested as part of calling function
def post_validation_ip2dev(ip2dev: dict, sim_ifaces: dict):
    parsed_ips = len(ip2dev.keys())
    topo_ips = 0

    for dev_ifaces in sim_ifaces.values():
        topo_ips += len(dev_ifaces.keys())

    if parsed_ips != topo_ips:
        raise ValueError("Suspected repeated IP addresses in topology")


def post_validation_networks(topo_networks: list, sim_networks: list):
    if len(topo_networks) != len(sim_networks):
        raise ValueError("Network number mismatch between topo file and networks.log")


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
