import csv
import json
from ast import literal_eval as make_tuple
from collections import OrderedDict
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


strategies_full = {"bfs": "BFS", "dfs": "DFS",
                   "ph": "Path heuristic", "nh": "Neighbor heuristic"}
property_types = ["reach", "iso"]
properties = {
    "ctree": {
        "reach": 30,
        "iso": 12
    },
    "hiberniaus": {
        "reach": 60,
        "iso": 30
    },
    "bics": {
        "reach": 80,
        "iso": 50
    }
}


def read_search_plan(search_plan_file: str) -> list:
    with open(search_plan_file) as f:
        raw_states = f.readlines()

    raw_states = [x.strip() for x in raw_states]

    tuple_states = []

    for s in raw_states:
        tuple_states.append(sorted(make_tuple(s)))

    return tuple_states


def get_prop_violations(topo_name: str, prop_type: str, num_props: int) -> OrderedDict:
    raw_violations = read_full_topo_violations(topo_name)
    all_violations = raw_violations[prop_type]["DFS"]
    prop_violations = OrderedDict()

    for prop_id in range(1, num_props + 1):
        prop_violations.setdefault(prop_id, [])

    for iter_num, iter_props in all_violations.items():
        for prop_id in iter_props:
            prop_violations[prop_id].append(iter_num)

    return prop_violations


def read_full_topo_violations(topo_name: str):
    all_violations = {
        "reach": dict(),
        "iso": dict()
    }

    for vio_type in property_types:
        bfs_violations: list = read_full_violations_log(topo_name, vio_type)
        all_violations[vio_type].update({"DFS": bfs_violations})

    return all_violations


def read_full_violations_log(topo_name: str, vio_type: str) -> OrderedDict:
    log_dir = "{}/{}".format(const.VIOLATIONS_DIR, topo_name)
    filename = "{}_violations_dfs.log".format(vio_type)
    filepath = "{}/{}".format(log_dir, filename)

    violations = OrderedDict()

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')

        for row in csv_reader:
            iteration = int(row[0])
            violated_props = list(map(int, row[1].split(",")))

            violations.update({iteration: violated_props})

    return violations


def find_property_violations(prop_violations, old_plan, new_plan):
    new_violations = dict()

    for prop_id, old_violating_states in prop_violations.items():
        new_violating_states = []

        for violating_state_id in old_violating_states:
            # find the actual state that violated the property
            violating_state = old_plan[violating_state_id - 1]
            # find the index of the same state in the new plan
            new_state_id = new_plan.index(violating_state) + 1

            new_violating_states.append(new_state_id)

        if new_violating_states:
            first_to_violate = min(new_violating_states)
            new_violations.setdefault(first_to_violate, []).append(prop_id)

    return new_violations


def pretty_print_violating_states(violating_states: dict):
    violating_state_ids = list(violating_states.keys())
    violating_state_ids.sort()

    for state_id in violating_state_ids:
        violated_props = violating_states[state_id]
        print("{}:{}".format(state_id, ",".join(str(x) for x in violated_props)))


def main():
    topology = "bics"
    property_type = "iso"
    num_props = properties[topology][property_type]

    plan_path1 = "/home/pesho/D/search_plan_bics_dfs.log"
    plan_path2 = "/home/pesho/D/search_plan_bics_ph.log"

    prop_violations = get_prop_violations(topology, property_type, num_props)
    old_plan = read_search_plan(plan_path1)
    new_plan = read_search_plan(plan_path2)

    new_violating_states = find_property_violations(prop_violations, old_plan, new_plan)
    pretty_print_violating_states(new_violating_states)


main()
