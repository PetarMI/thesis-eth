from subprocess import call
from termcolor import colored as clr
import json
from fuzzer.controllers import reachability_parser as rp
from fuzzer.controllers.SearchPlan import SearchPlan
from fuzzer.controllers import StateTransition
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const
from fuzzer.common import file_writer as fw
from fuzzer.verifiers import reachability_verifier as rv


class Fuzzer:
    def __init__(self):
        # reads all data for running devices during fuzzing
        self.fuzz_data = FuzzData()

        # declare all state variables used during fuzzing
        self.search_plan: list = None
        self.search_stats: dict = None
        self.transition = None
        self.properties: list = None
        # potentially to be used in gen_state_change
        # self.fail_type = "iface"

    def prepare_fuzzing(self, depth: int, algo: str):
        self.properties = rp.parse_properties(self.fuzz_data)

        # generate the search strategy/statespace
        nets: list = self.fuzz_data.get_networks()
        planner = SearchPlan(depth, nets)
        self.search_plan = planner.get_search_plan(algo)
        self.search_stats = planner.get_fuzzing_stats()

        # set fuzzing approach state variables
        self.transition = StateTransition.FullRevert()

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

            print(clr("#### Testing reachability", 'cyan', attrs=['bold']))
            exec_ping_reachability()

            print(clr("#### Verifying properties", 'cyan', attrs=['bold']))
            self.verify_properties(state)

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

    def verify_properties(self, state: tuple):
        ver_results: dict = rv.verify_ping_reachability(self.properties)
        all_successful: bool = True
        failures = []

        for property_id, ver_res in ver_results.items():
            if ver_res["status"] == 0:
                continue
            else:
                all_successful = False

            col, desc = pretty_print_failure(property_id, ver_res)
            failures.append({
                "pid": property_id,
                "state": state,
                "desc": desc,
            })

            print(clr(desc, col))

        if all_successful:
            print(clr("All properties HOLD", 'green'))

        fw.write_state_failures(failures)

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


def pretty_print_failure(pid: int, verification_res: dict):
    ver_status = verification_res["status"]

    if ver_status == 1:
        return 'red', "Property {} FAILED: {}".format(pid, verification_res["desc"])
    if ver_status == 2:
        return 'yellow', "Property {} WARNING: {}".format(pid, verification_res["desc"])
    if ver_status == 3:
        return 'grey', "Property {} ERROR: {}".format(pid, verification_res["desc"])


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
