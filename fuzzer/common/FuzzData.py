""" Fuzzing data collection

The purpose of this class is to collect all fuzzing data
and parse it to a representation which is efficient to use
during fuzzing.

How to use: Other modules should import just the class via
            from fuzzer.common.FuzzData import FuzzData
"""

from fuzzer.common import file_reader as fr


class FuzzData:
    def __init__(self):
        topo: dict = fr.read_topo()
        self._topo_name = topo["meta"]["name"]
        self._networks = topo["networks"]
        self._containers: dict = parse_containers(topo)
        self._vms = fr.read_vm_info()

    @property
    def topo_name(self) -> dict:
        return self._topo_name

    @property
    def networks(self) -> list:
        return self._networks

    @property
    def containers(self) -> dict:
        return self._containers

    @property
    def vms(self):
        return self._vms


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
