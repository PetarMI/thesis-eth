from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class InstructionGenerator:
    def __init__(self, fuzz_data: FuzzData):
        self.fuzz_data = fuzz_data

    def gen_transition_instructions(self, link_changes: dict) -> dict:
        instructions = {}
        instructions.update({"restore": []})
        instructions.update({"drop": []})

        for op_type, links in link_changes.items():
            for link in links:
                link_instructions: list = self.get_link_instructions(op_type, link)
                instructions.setdefault(op_type, []).extend(link_instructions)

        return instructions

    def get_link_instructions(self, op_type: str, link: str) -> list:
        instructions = []
        link_containers: list = self.fuzz_data.find_network_devices(link)

        for dev in link_containers:
            dev_instr = dict()

            dev_instr["link"] = link
            dev_instr["op_type"] = op_type
            dev_instr["vm"] = self.fuzz_data.find_container_vm(dev)
            dev_instr["container"] = dev
            dev_instr["iface"] = self.fuzz_data.find_network_interface(dev, link)

            instructions.append(dev_instr)

        return instructions

    def get_transition_data(self, link_changes: dict):
        trans_data = dict()

        trans_data[const.DROP] = self.get_link_ips(link_changes[const.DROP])
        trans_data[const.RESTORE] = self.get_link_devices(link_changes[const.RESTORE])

        return trans_data

    def get_link_ips(self, networks: list) -> list:
        """ Get the IPs of a list of network names """
        ips = []

        for net in networks:
            ips.append(self.fuzz_data.get_sim_net_ip(net))

        return ips

    def get_link_devices(self, networks: list) -> list:
        affected_containers = []

        for net_name in networks:
            # net_name: str = self.fuzz_data.get_sim_net_name(net_ip)
            net_devices: list = self.fuzz_data.find_network_devices(net_name)

            affected_containers.extend(net_devices)

        affected_containers = list(set(affected_containers))

        return affected_containers
