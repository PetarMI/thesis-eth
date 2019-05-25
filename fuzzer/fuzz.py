from argparse import ArgumentParser
from fuzzer.controllers.SearchPlan import SearchPlan
from fuzzer.controllers import reachability_parser as rp
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import fuzz_data_ops as fdata_ops
import json


def main(depth: int, algo: str):
    # reads all data for running devices and containers during fuzzing
    fuzz_data = FuzzData()
    search_plan: list = prepare_fuzzing(fuzz_data, depth, algo)

    # execute fuzzing according to generated search plan
    fuzz(search_plan)


def prepare_fuzzing(fuzz_data: FuzzData, depth: int, algo: str) -> list:
    # parse the properties we will be checking during fuzzing
    rp.parse_properties(fuzz_data)

    # generate a search strategy
    nets: list = fdata_ops.get_network_names(fuzz_data.get_networks())
    planner = SearchPlan(depth, nets)
    search_plan = planner.get_search_plan(algo)
    search_stats = planner.get_fuzzing_stats()
    print(json.dumps(search_stats, indent=4))

    return search_plan


def fuzz(statespace: list):
    dropped_links = []

    for state in statespace:
        print("STATE: {}".format(state))
        state_changes: dict = find_state_changes(dropped_links, state)
        exec_state_change(state_changes)
        dropped_links = state
        print("===================================")


# @Tested
def find_state_changes(dropped_links: list, next_state: tuple) -> dict:
    links_to_restore = state_diff(dropped_links, next_state)
    links_to_drop = state_diff(next_state, dropped_links)

    return {
        "restore": links_to_restore,
        "drop": links_to_drop
    }


# @Tested composite `find_state_changes`
def state_diff(stateA, stateB) -> list:
    """ Difference between two lists/tuples (elements that are in A but not B)
    Preferred to setA.difference(setB) since the later is non-deterministic
    Later may be asymptotically faster but here we will only diff lists of 2-3 elements
    """
    diff = []

    for state in stateA:
        if state not in stateB:
            diff.append(state)

    return diff


def exec_state_change(state_changes: dict):
    exec_restore(state_changes["restore"])
    exec_drop(state_changes["drop"])


def exec_drop(links: list):
    for link in links:
        print("Dropped link: {}".format(link))


def exec_restore(links: list):
    for link in links:
        print("Restored link: {}".format(link))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", dest="depth", required=True,
                        help="The max depth we are checking for failed links")
    parser.add_argument("-a", "--algo", dest="algo", required=True,
                        help="Search algorithm to use")
    args = parser.parse_args()

    main(int(args.depth), args.algo)
