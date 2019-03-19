import json
import yaml
from argparse import ArgumentParser
import topo_parser as tp
import constants as const


class ComposeGenerator():

    def __init__(self, topology_file: str):
        self.topo: dict = import_topo(topology_file)
        self.topo_meta = tp.find_metadata(self.topo)
        self.frr_containers: list = tp.find_containers(self.topo, "frr")
        self.topo_nets: list = tp.find_nets(self.topo)

    def compose(self):
        topo_compose: dict = {}
        self.write_version(topo_compose)
        self.write_frr_containers(topo_compose)
        self.write_nets(topo_compose)
        self.write_docker_compose(topo_compose)

    def write_version(self, topo_compose: dict) -> dict:
        version = self.topo_meta.get("version", "3.7")

        topo_compose.update({"version": version})

        return topo_compose

    def write_frr_containers(self, topo_compose: dict) -> dict:
        containers = {}

        for c in self.frr_containers:
            c_ifaces = write_container_ifaces(c.get("interfaces"))
            c_name = self.topo_meta.get("name") + "-" + c.get("name")
            c_volumes = write_container_volumes()

            containers.update({
                c.get("name"): {
                    "image": "phynet:1.0",
                    "container_name": c_name,
                    "hostname": c.get("name"),
                    "privileged": True,
                    "volumes": c_volumes,
                    "networks": c_ifaces
                }
            })

        topo_compose.update({"services": containers})

        return topo_compose

    def write_nets(self, topo_compose: dict) -> dict:
        nets = {}

        for net in self.topo_nets:
            nets.update({
                net.get("name"): {
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
                }
            })

        topo_compose.update({"networks": nets})

        return topo_compose

    def write_docker_compose(self, topo_compose: dict):
        topo_name = self.topo_meta.get("name")
        compose_file = const.TOPO_DIR + topo_name + "/" + const.DOCKER_COMPOSE

        with open(compose_file, 'w') as docker_compose:
            yaml.dump(topo_compose, docker_compose,
                      default_flow_style=False, sort_keys=False)


def import_topo(topo_name: str) -> dict:
    """ Function to load the topology encoded in json format """
    # topo_file: str = const.TOPO_DIR + topo_name + const.TOPO_EXTENSION

    with open(topo_name) as json_data:
        topo = json.load(json_data)

    return topo


def write_container_ifaces(cont_interfaces: list) -> dict:
    ifaces = {}

    for iface in cont_interfaces:
        ifaces.update({
            iface.get("network"): {
                "ipv4_address": iface.get("ipaddr")
            }
        })

    return ifaces


def write_container_volumes() -> list:
    volumes = [{
        "type": "bind",
        "source": "./configs",
        "target": "/home/configs"
    }]

    return volumes


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.filename

    composer = ComposeGenerator(topo_name)
    composer.compose()
