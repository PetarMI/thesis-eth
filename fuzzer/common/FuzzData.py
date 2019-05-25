""" Fuzzing data collection

The purpose of this class is to be a wrapper around all fuzzing data.
All info which will be frequently accessed is kept in memory and
restructured via the static methods so that they have a primary key that
allows quick search. Other data is simply read from file as if the caller
uses the file_reader.

How to use: Other modules should import just the class via
            from fuzzer.common.FuzzData import FuzzData
"""

from fuzzer.common import file_reader as fr


class FuzzData:
    def __init__(self):
        topo: dict = fr.read_topo()
        raw_nets: dict = fr.read_sim_networks()
        self.containers: dict = parse_containers(topo)
        self.net2dev: dict = parse_net2devices(topo["meta"]["name"],
                                               topo["containers"])

    # in-memory data
    def get_containers(self) -> dict:
        return self.containers

    def get_net2dev(self) -> dict:
        return self.net2dev

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


def parse_containers(topo: dict) -> dict:
    """ Parse the containers into a dict so we have the container name as
        a primary key when searching.
    """
    containers = dict()

    for container in topo["containers"]:
        containers.update({
            container["name"]: {
                "vm": container["vm"],
                "interfaces": container["interfaces"]
            }
        })

    return containers


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


# @Tested as part of calling function
def net2dev_post_validation(net2dev: dict):
    """ Verify that a link has at most two connected devices """
    for net, containers in net2dev.items():
        if len(containers) > 2:
            raise ValueError("More than two containers connected to network {}"
                             .format(net))


def prepend_topo(topo_name: str, entity: str) -> str:
    return "{}-{}".format(topo_name, entity)
