from argparse import ArgumentParser
from subprocess import call
from termcolor import colored as clr
import json
from fuzzer.controllers.SearchPlan import SearchPlan
from fuzzer.controllers import reachability_parser as rp
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const
from fuzzer.verifiers import reachability_verifier as rv
from fuzzer.common import file_writer as fw


class Fuzzer:
    def __init__(self):
        # reads all data for running devices and containers during fuzzing
        self.fuzz_data = FuzzData()
        self.search_plan: list = None
        self.search_stats: dict = None
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

    def fuzz(self):
        dropped_links = []

        for n, state in enumerate(self.search_plan):
            print(clr("State {}/{}: {}".format(n, self.search_stats["total"], state),
                      'green', attrs=['bold']))
            print(clr("Failed networks: {}".format(self.get_network_ips(state)),
                      'magenta'))

            link_changes: dict = self.find_link_changes(dropped_links, state)
            state_change_instr = self.gen_state_change(link_changes)

            print(clr("## Executing link changes", 'cyan', attrs=['bold']))
            exec_state_change(state_change_instr)

            print(clr("## Waiting for fib convergence", 'cyan', attrs=['bold']))
            exec_convergence_wait()

            print(clr("## Testing reachability", 'cyan', attrs=['bold']))
            exec_reachability_testing()

            print(clr("## Verifying properties", 'cyan', attrs=['bold']))
            self.verify_properties(state)

            dropped_links = state

            print("===================================")

    # @Tested
    @staticmethod
    def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
        links_to_restore = state_diff(dropped_links, next_state)
        links_to_drop = state_diff(next_state, dropped_links)

        return {
            "restore": links_to_restore,
            "drop": links_to_drop
        }

    def gen_state_change(self, link_changes: dict) -> list:
        instructions = []

        for op_type, links in link_changes.items():
            for link in links:
                link_instructions: list = self.get_link_instructions(op_type, link)
                instructions.extend(link_instructions)

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
        ver_results: dict = rv.verify_reachability(self.properties)
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

    def get_network_ips(self, nets):
        ips = []

        for net in nets:
            ips.append(self.fuzz_data.get_sim_net_ip(net))

        return ips


def exec_state_change(instructions: list):
    """ Call an executor script to execute each change
    Either pass params directly OR write to file where script reads from
    """
    for n, instr in enumerate(instructions, start=1):
        pretty_print_instr(instr, n, len(instructions))
        return_code: int = call([const.LINK_STATE_SH, "-f", "iface",
                                 "-v", instr["vm"], "-d", instr["container"],
                                 "-i", instr["iface"], "-s", instr["op_type"]])
        signal_script_fail(return_code, "{} interface {}".
                           format(instr["op_type"], instr["iface"]))


def exec_convergence_wait():
    #input("Press Enter to continue...")
    return_code: int = call([const.CONVERGENCE_SH])
    signal_script_fail(return_code)


def exec_reachability_testing():
    return_code: int = call([const.PING_SH])
    signal_script_fail(return_code)


# @Tested composite `find_state_changes`
def state_diff(state_a, state_b) -> list:
    """ Difference between two lists/tuples (elements that are in A but not B)
    Preferred to setA.difference(setB) since the later is non-deterministic
    Later may be asymptotically faster but here we will only diff lists of 2-3 elements
    """
    diff = []

    for state in state_a:
        if state not in state_b:
            diff.append(state)

    return diff


def pretty_print_instr(instr: dict, n, t):
    progress = "({}/{})".format(n, t)
    op = "Dropping" if instr["op_type"] == "drop" else "Restoring"

    print("{} {} link {} on device {}".
          format(progress, op, instr["link"], instr["container"]))


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


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", dest="depth", required=False,
                        help="The max depth we are checking for failed links")
    parser.add_argument("-a", "--algo", dest="algo", required=False,
                        help="Search algorithm to use")
    args = parser.parse_args()

    fuzzer = Fuzzer()
    fuzzer.prepare_fuzzing(3, "bfs")
    fuzzer.print_search_strategy()
    fuzzer.fuzz()
