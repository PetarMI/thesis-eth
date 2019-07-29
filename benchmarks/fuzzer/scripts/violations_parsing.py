import csv
import json
import matplotlib.pyplot as plt
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


def parse_prop_difficulty(raw_violations: dict, num_props: int) -> OrderedDict:
    all_violations = raw_violations["DFS"]
    prop_difficulties = OrderedDict()

    for prop_id in range(1, num_props + 1):
        prop_difficulties.setdefault(prop_id, 0)

    for iter_props in all_violations.values():
        for prop_id in iter_props:
            prop_difficulties[prop_id] += 1

    not_violated = 0

    for num_violated in prop_difficulties.values():
        if num_violated == 0:
            not_violated += 1

    print("Number of properties not violated: {}".format(not_violated))

    return prop_difficulties


def normalize_topo_violations(parsed_violations: dict) -> dict:
    violations = dict()

    for strat, strat_results in parsed_violations.items():
        normalized_violations = OrderedDict()
        last_iteration = 1
        last_num_violations = 0

        for iteration, iter_violations in strat_results.items():
            while last_iteration < iteration:
                normalized_violations.update({last_iteration: last_num_violations})
                last_iteration += 1

            normalized_violations.update({iteration: iter_violations})
            last_num_violations = iter_violations

        violations.update({strat: normalized_violations})

    return violations


def parse_topo_violations(raw_violations: dict) -> dict:
    violations = dict()

    for strat, strat_results in raw_violations.items():
        violated_properties = set([])
        parsed_strategy_results = OrderedDict()

        for iteration, iter_violations in strat_results.items():
            old_num_violations = len(violated_properties)
            violated_properties.update(iter_violations)

            if old_num_violations != len(violated_properties):
                parsed_strategy_results.update({iteration: len(violated_properties)})

        violations.update({strat: parsed_strategy_results})

    return violations


def read_topo_violations(topo_name: str):
    all_violations = {
        "reach": dict(),
        "iso": dict()
    }

    for vio_type in property_types:
        for strat_code, strat in strategies_full.items():
            try:
                strat_violations: list = read_violations_log(topo_name, vio_type, strat_code)
                all_violations[vio_type].update({strat: strat_violations})
            except FileNotFoundError:
                continue

    return all_violations


def read_violations_log(topo_name: str, vio_type: str, strat: str) -> OrderedDict:
    log_dir = "{}/{}".format(const.VIOLATIONS_DIR, topo_name)
    filename = "{}_violations_{}.log".format(vio_type, strat)
    filepath = "{}/{}".format(log_dir, filename)

    violations = OrderedDict()

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')

        for row in csv_reader:
            iteration = int(row[0])
            violated_props = list(map(int, row[1].split(",")))

            violations.update({iteration: violated_props})

    return violations


def make_violations_plot(violations: dict):
    fig, ax = plt.subplots()

    for s, v in violations.items():
        plt.plot(list(v.keys()), list(v.values()), label=s)

    plt.ylabel('Properties violated')
    plt.xlabel("Number of iterations")
    ax.set_title('Property violations comparison')
    plt.legend()

    plt.show()


def make_difficulty_plot(difficulties: OrderedDict):
    fig, ax = plt.subplots()

    plt.plot(list(difficulties.keys()), list(difficulties.values()),
             marker='o')

    plt.ylabel('Number of violating states')
    plt.xlabel("Properties")
    ax.set_title('Property violations comparison')

    plt.show()


def plot_topo_violations(topo_name: str, prop_type: str):
    raw_violations = read_topo_violations(topo_name)
    parsed_violations = parse_topo_violations(raw_violations[prop_type])
    normalized_violations = normalize_topo_violations(parsed_violations)
    make_violations_plot(normalized_violations)


def plot_topo_properties_difficulty(topo_name: str, prop_type: str, num_props: int):
    raw_violations = read_topo_violations(topo_name)
    parsed_difficulty = parse_prop_difficulty(raw_violations[prop_type], num_props)
    make_difficulty_plot(parsed_difficulty)


def main():
    topology = "bics"
    property_type = "reach"
    num_props = properties[topology][property_type]

    # plot_topo_violations(topology, property_type)
    plot_topo_properties_difficulty(topology, property_type, num_props)


main()
