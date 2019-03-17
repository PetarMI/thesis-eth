import json
import yaml
from argparse import ArgumentParser
import constants as const
import topo_parser as tp


def main(topology_file: str):
    topo: dict = import_topo(topology_file)
    topo_meta = tp.find_metadata(topo)
    frr_containers: list = tp.find_containers(topo, "frr")
    topo_nets: list = tp.find_nets(topo)

    topo_compose: dict = {}
    write_version(topo_meta, topo_compose)
    write_containers(frr_containers, topo_compose)
    write_nets(topo_nets, topo_compose)
    write_docker_compose(topo_meta, topo_compose)


def import_topo(topo_name: str) -> dict:
    """ Function to load the topology encoded in json format """
    # topo_file: str = const.TOPO_DIR + topo_name + const.TOPO_EXTENSION

    with open(topo_name) as json_data:
        topo = json.load(json_data)

    return topo


def write_version(topo_meta: dict, topo_compose: dict) -> dict:
    version = topo_meta.get("version", "3.7")

    topo_compose.update({"version": version})

    return topo_compose


def write_containers(topo_containers: list, topo_compose: dict) -> dict:
    containers = {}

    for c in topo_containers:
        c_ifaces = write_container_ifaces(c.get("interfaces"))

        containers.update({
            c.get("name"): {
                "image": "docker:dind",
                #"container_name": c.get("name"),
                "privileged": True,
                "networks": c_ifaces
            }
        })

    topo_compose.update({"services": containers})

    return topo_compose


def write_container_ifaces(cont_interfaces: list) -> dict:
    ifaces = {}

    for iface in cont_interfaces:
        ifaces.update(
            {iface.get("network"): {
                "ipv4_address": iface.get("ipaddr")
            }})

    return ifaces


def write_nets(topo_nets: list, topo_compose: dict) -> dict:
    nets = {}

    for net in topo_nets:
        nets.update(
            {net.get("name"): {
                "driver": "bridge",
                "attachable": True,
                "ipam": {
                    "driver": "default",
                    "config": [
                        {
                            "subnet": net.get("subnet")
                        }
                    ]
                }
            }})

    topo_compose.update({"networks": nets})

    return topo_compose


def write_docker_compose(topo_meta: dict, topo_compose: dict):
    topo_name = topo_meta.get("name")
    compose_file = const.TOPO_DIR + topo_name + "/" + const.DOCKER_COMPOSE

    with open(compose_file, 'w') as docker_compose:
        yaml.dump(topo_compose, docker_compose,
                  default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.filename
    main(topo_name)
