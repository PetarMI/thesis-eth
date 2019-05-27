from argparse import ArgumentParser
from fuzzer.controllers.SearchPlan import SearchPlan
from fuzzer.controllers import reachability_parser as rp
from fuzzer.common.FuzzData import FuzzData
import json


# TODO: potentially will become a class if more variables are introduced
def main(depth: int, algo: str):
    # reads all data for running devices and containers during fuzzing
    fuzz_data = FuzzData()
    search_plan: list = prepare_fuzzing(fuzz_data, depth, algo)

    # execute fuzzing according to generated search plan
    fuzz(fuzz_data, search_plan)


def prepare_fuzzing(fuzz_data: FuzzData, depth: int, algo: str) -> list:
    # parse the properties we will be checking during fuzzing
    rp.parse_properties(fuzz_data)

    # generate a search strategy
    nets: list = fuzz_data.get_networks()
    planner = SearchPlan(depth, nets)
    search_plan = planner.get_search_plan(algo)
    search_stats = planner.get_fuzzing_stats()
    print(json.dumps(search_stats, indent=4))

    return search_plan


def fuzz(fuzz_data: FuzzData, statespace: list):
    dropped_links = []

    for state in statespace:
        print("STATE: {}".format(state))

        link_changes: dict = find_link_changes(dropped_links, state)
        state_change_instr = gen_state_change(fuzz_data, link_changes)
        pretty_print_instr(state_change_instr)
        # exec_state_changes(state_change_instr)
        dropped_links = state

        print("===================================")


# @Tested
def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
    links_to_restore = state_diff(dropped_links, next_state)
    links_to_drop = state_diff(next_state, dropped_links)

    return {
        "restore": links_to_restore,
        "drop": links_to_drop
    }


def gen_state_change(fuzz_data: FuzzData, link_changes: dict) -> list:
    instructions = []

    for op_type, links in link_changes.items():
        for link in links:
            link_instructions: list = get_link_instructions(fuzz_data, op_type, link)
            instructions.extend(link_instructions)

    return instructions


def exec_state_change(instructions: list):
    """ Call an executor script to execute each change
    Either pass params directly OR write to file where script reads from
    """
    raise ValueError("Not implemented")


def get_link_instructions(fuzz_data: FuzzData, op_type: str, link: str) -> list:
    instructions = []
    link_containers: list = fuzz_data.find_network_devices(link)

    for dev in link_containers:
        dev_instr = dict()

        dev_instr["link"] = link
        dev_instr["op_type"] = op_type
        dev_instr["vm"] = fuzz_data.find_container_vm(dev)
        dev_instr["container"] = dev
        dev_instr["iface"] = fuzz_data.find_network_interface(dev, link)

        instructions.append(dev_instr)

    return instructions


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


def pretty_print_instr(instructions: list):
    for instr in instructions:
        print("{} link: {}, VM: {}, DEV: {}, IFACE: {}".
              format(instr["op_type"], instr["link"], instr["vm"],
                     instr["container"], instr["iface"]))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", dest="depth", required=True,
                        help="The max depth we are checking for failed links")
    parser.add_argument("-a", "--algo", dest="algo", required=True,
                        help="Search algorithm to use")
    args = parser.parse_args()

    main(int(args.depth), args.algo)
