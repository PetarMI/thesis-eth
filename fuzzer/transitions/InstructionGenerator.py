import random
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class InstructionGenerator:
    def __init__(self, fuzz_data: FuzzData):
        self.fuzz_data = fuzz_data
        self.link2dev = dict()

    def gen_transition_instructions(self, link_changes: dict) -> dict:
        instructions = {}
        instructions.update({"restore": []})
        instructions.update({"drop": []})

        for op_type, links in link_changes.items():
            for link in links:
                link_instruction: dict = self.get_link_instruction(op_type, link)
                instructions.setdefault(op_type, []).append(link_instruction)

        return instructions

    def get_link_instruction(self, op_type: str, link: str) -> dict:
        dev = self.pick_link_device(link, op_type)
        dev_instr = dict()

        dev_instr["link"] = link
        dev_instr["op_type"] = op_type
        dev_instr["vm"] = self.fuzz_data.find_container_vm(dev)
        dev_instr["container"] = dev
        dev_instr["iface"] = self.fuzz_data.find_network_interface(dev, link)

        return dev_instr

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
            net_device: str = self.pick_link_device(net_name, const.RESTORE)

            affected_containers.append(net_device)

        return list(set(affected_containers))

    def pick_link_device(self, link: str, op_type: str) -> str:
        dev: str = self.link2dev.get(link, None)

        if op_type == const.DROP:
            check_none(dev, True, "Device {} for link {} exists in logs"
                       .format(dev, link))
            link_containers: list = self.fuzz_data.find_network_devices(link)
            dev = random.choice(link_containers)
            self.link2dev.update({link: dev})
        elif op_type == const.RESTORE:
            check_none(dev, False, "Device {} for link {} doesn't exists in logs"
                       .format(dev, link))

        return dev


def check_none(item, expected, msg):
    res = False

    if item is None:
        res = True

    if res != expected:
        raise ValueError(msg)
