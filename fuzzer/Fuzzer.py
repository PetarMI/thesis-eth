from subprocess import call
from termcolor import colored as clr
import json
from fuzzer.controllers import property_parser as pp
from fuzzer.controllers.Statespace import Statespace
from fuzzer.controllers import StateTransition
from fuzzer.controllers import Verification as Ver
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Fuzzer:
    def __init__(self):
        # reads all data for running devices during fuzzing
        self.fuzz_data = FuzzData()

        # declare all state variables used during fuzzing
        self.search_plan: list = None
        self.search_stats: dict = None
        self.transition = None
        self.verification = None

    def prepare_fuzzing(self, depth: int):
        # define necessary variables
        nets: list = self.fuzz_data.get_networks()
        statespace = Statespace(depth, nets)
        properties: list = pp.parse_properties(self.fuzz_data)

        # set fuzzing approach state variables
        self.search_plan = statespace.get_heuristic_plan(properties, self.fuzz_data)
        self.search_stats = statespace.get_fuzzing_stats()
        self.transition = StateTransition.PartialRevert(self.fuzz_data)
        self.verification = Ver.Verification(properties, self.fuzz_data)

    def verify_deployment(self):
        print(clr("#### Verifying deployment", 'cyan', attrs=['bold']))
        exec_ping_reachability()
        ping_results: dict = self.verification.verify_ping_reachability()
        self.verification.interpret_ping_results(ping_results)

    def fuzz(self):
        dropped_links = []

        for n, state in enumerate(self.search_plan):
            print(clr("State {}/{}: {}".format(n, self.search_stats["total"], state),
                      'green', attrs=['bold']))
            print(clr("Failed networks: {}".format(self.get_network_ips(state)),
                      'magenta'))

            link_changes: dict = self.transition.find_link_changes(dropped_links, state)
            transition_instr: dict = self.gen_transition_instructions(link_changes)

            print(clr("#### Executing state transition", 'cyan', attrs=['bold']))
            net_changes: dict = self.get_link_change_ips(link_changes)
            self.transition.exec_state_transition(transition_instr, net_changes)

            print(clr("#### Verifying properties", 'cyan', attrs=['bold']))
            fib_results: dict = self.verification.verify_fib_reachability()
            self.verification.interpret_fib_results(state, fib_results)

            dropped_links = state

            print("===================================")

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

    def print_search_strategy(self):
        print(clr("## Statespace stats", 'magenta', attrs=['bold']))
        print(json.dumps(self.search_stats, indent=4))

    def get_link_change_ips(self, link_changes: dict):
        """ Take the link changes and return same format but with IPs
        instead of names """
        ip_changes = {}

        for op_type in link_changes.keys():
            links_ips: list = self.get_network_ips(link_changes.get(op_type))
            ip_changes.update({op_type: links_ips})

        return ip_changes

    def get_network_ips(self, nets) -> list:
        """ Get the IPs of a list of network names """
        ips = []

        for net in nets:
            ips.append(self.fuzz_data.get_sim_net_ip(net))

        return ips


def exec_ping_reachability():
    return_code: int = call([const.PING_SH])
    signal_script_fail(return_code)


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
