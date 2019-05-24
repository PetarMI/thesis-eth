""" Fuzzing data operations

This script collects all operations for finding something in the
fuzzing data, i.e. data of the running containers.

How to use: All functions are implemented to work on the data format
            stored in the fuzzer.common.FuzzData class
"""


def get_networks(topo_networks: list) -> list:
    """ Get a list of all network names """
    nets = []

    for net in topo_networks:
        nets.append(net["name"])

    return nets


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
