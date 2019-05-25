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
        self._containers: dict = parse_containers(topo)

    def get_topo_name(self) -> dict:
        topo: dict = fr.read_topo()
        return topo["meta"]["name"]

    def get_networks(self) -> list:
        topo: dict = fr.read_topo()
        return topo["networks"]

    def get_containers(self) -> dict:
        return self._containers

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
