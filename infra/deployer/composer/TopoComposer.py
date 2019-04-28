from argparse import ArgumentParser
import os
import topo_parser as tp
import constants_composer as const


class TopoComposer:

    def __init__(self, topo_name: str):
        topology_file = "{0}/{1}/{1}.topo".format(const.TOPO_DIR, topo_name)
        self.topo: dict = tp.import_topo(topology_file)
        self.topo_name = tp.find_topo_name(self.topo)

    def gen_compose_files(self):
        print("##### Generating compose files #####")
        nets: list = self.parse_nets()
        containers: dict = self.parse_containers()

        self.write_compose_files(nets, containers)
        print("##### Done. #####")

    def parse_nets(self) -> list:
        """
        :return: A list of networks that are used in the topology
        """
        topo_nets: list = tp.find_nets(self.topo)
        nets = []

        for net in topo_nets:
            net_name = self.prepend_topo(tp.safe_get(net, "name"))
            nets.append(net_name)

        return nets

    def parse_containers(self) -> dict:
        """ Parse the per VM container instructions

        :return: A dictionary of VMs and their belonging containers as a list
        """
        topo_containers = tp.find_containers(self.topo)
        vms = {}

        for cont in topo_containers:
            vm = tp.safe_get(cont, "vm")
            parsed_container = self.parse_container(cont)

            vms.setdefault(vm, []).append(parsed_container)

        return vms

    def parse_container(self, container: dict) -> dict:
        """ Parse every Layer 2 container into an intermediate representation

        :param container: A piece of the .topo file describing the container
        :return: The intermediate representation of the container in dict format
        """
        container_nets = tp.find_container_nets(container)
        # prepend the topo name to every network
        container_nets = list(map(lambda x: self.prepend_topo(x), container_nets))

        formatted_cont = {
            "name": self.prepend_topo(tp.safe_get(container, "name")),
            "image": tp.get_container_image(tp.safe_get(container, "type")),
            "mainnet": container_nets[0],
            "nets": container_nets[1:]
        }

        return formatted_cont

    def write_compose_files(self, nets: list, containers: dict):
        """ Entry function for writing all the compose files

        :param nets: List of networks used in the topology
        :param containers: Containers used in the topology spread by VM
        :return:
        """
        output_dir = "{}/{}{}".format(const.DPL_FILES_DIR,
                                      self.topo_name, const.COMPOSE_DIR)
        os.makedirs(output_dir, exist_ok=True)

        print("Writing networks file...")
        write_nets(nets, output_dir)
        write_containers(containers, output_dir)

    def prepend_topo(self, obj) -> str:
        """ Prepend the topology name to a network or container """
        return "{}-{}".format(self.topo_name, obj)


def write_nets(nets: list, output_dir: str):
    """ Write the network as a column in a .csv file"""
    filename = "{}/{}".format(output_dir, const.NET_COMPOSE_FILE)
    write_file(filename, nets)


def write_containers(vms: dict, output_dir):
    """ Write the per VM containers as a set of instructions to the VM and
    save to file.

    :param vms: Dict of VMs mapping to a list of containers
    :param output_dir: where to save the output files
    :return:
    """
    # iterate over each VM
    for vm, containers in vms.items():
        print("Writing compose files for VM {}".format(vm))
        create_commands = []
        connect_commands = []

        # iterate over each container of a VM
        for cont in containers:
            create = "{},{},{}".format(cont.get("name"), cont.get("mainnet"),
                                       cont.get("image"))
            create_commands.append(create)

            for net in cont.get("nets"):
                connect = "{},{}".format(net, cont.get("name"))
                connect_commands.append(connect)

        create_file = "{}/{}{}_{}". \
            format(output_dir, const.VM_NAME, vm, const.CONTAINER_COMPOSE_FILE)
        connect_file = "{}/{}{}_{}". \
            format(output_dir, const.VM_NAME, vm, const.LINKS_COMPOSE_FILE)

        write_file(create_file, create_commands)
        write_file(connect_file, connect_commands)


def write_file(filename: str, instr: list):
    """ Auxiliary function for writing a list of instructions to a file """
    with open(filename, 'w+', newline='') as file:
        for i in instr:
            file.write(i+"\n")


# def write_file2(filename: str, instr: list):
#    Write a list of instructions to a file without an empty line at end
#    with open(filename, 'w+', newline='') as file:
#        output = "\n".join(instr)
#        file.write(output)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology to be used for setup")
    args = parser.parse_args()

    topology_name: str = args.topology

    composer = TopoComposer(topology_name)
    composer.gen_compose_files()
