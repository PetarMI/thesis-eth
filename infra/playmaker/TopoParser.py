from argparse import ArgumentParser
import os
import csv
import topo_walker as tw
import constants as const

class TopoParser():

    def __init__(self, topology_file: str):
        self.topo: dict = tw.import_topo(topology_file)
        self.topo_name = tw.find_topo_name(self.topo)

    def parse_topology(self):
        nets: list = self.parse_nets()
        containers: list = self.parse_containers()

        self.write_compose_files(nets, containers)

    def parse_nets(self) -> list:
        topo_nets: list = tw.find_nets(self.topo)
        nets = []

        for net in topo_nets:
            net_name = self.prepend_topo(tw.safe_get(net, "name"))
            nets.append(net_name)

        return nets

    def parse_containers(self) -> list:

        topo_containers = tw.find_containers(self.topo)
        vms = {}

        for cont in topo_containers:
            vm = tw.safe_get(cont, "vm")
            parsed_container = self.parse_container(cont)

            vms.setdefault(vm, [])
            vms.get(vm).append(parsed_container)

        containers = []

        for vm in vms:
            containers.append(vms.get(vm))

        return containers

    def parse_container(self, container: dict) -> dict:
        container_nets = tw.find_container_nets(container)
        # prepend the topo name to every network
        container_nets = list(map(lambda x: self.prepend_topo(x), container_nets))

        formatted_cont = {
            "name": self.prepend_topo(tw.safe_get(container, "name")),
            "image": tw.get_container_image(tw.safe_get(container, "type")),
            "mainnet": container_nets[0],
            "nets": container_nets[1:]
        }

        return formatted_cont

    def write_compose_files(self, nets: list, containers: dict):
        output_dir = "{}/{}".format(const.COMPOSE_DIR, self.topo_name)
        os.makedirs(output_dir, exist_ok=True)

        write_nets(nets, output_dir)
        write_containers(containers, output_dir)

    def prepend_topo(self, obj) -> str:
        return "{}-{}".format(self.topo_name, obj)


def write_nets(nets: list, output_dir: str):
    filename = "{}/{}".format(output_dir, const.NET_FILE)
    write_file(filename, nets)


def write_containers(containers: dict, output_dir):
    for idx, vm in enumerate(containers):
        create_commands = []
        connect_commands = []

        for instr in vm:
            create = "{},{},{}".format(instr.get("name"), instr.get("mainnet"),
                                       instr.get("image"))
            create_commands.append(create)

            for net in instr.get("nets"):
                connect = "{},{}".format(net, instr.get("name"))
                connect_commands.append(connect)

        create_file = "{}/{}{}_{}{}".\
           format(output_dir, const.VM_NAME, idx, const.CREATE_FILE, const.FILE_EXT)
        connect_file = "{}/{}{}_{}{}".\
           format(output_dir, const.VM_NAME, idx, const.CONNECT_FILE, const.FILE_EXT)

        write_file(create_file, create_commands)
        write_file(connect_file, connect_commands)


def write_file(filename: str, instr: list):
    with open(filename, 'w+', newline='') as file:
        output = "\n".join(instr)
        file.write(output)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.filename

    composer = TopoParser(topo_name)
    composer.parse_topology()
