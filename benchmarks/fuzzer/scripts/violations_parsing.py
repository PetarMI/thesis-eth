import csv
import json
import matplotlib.pyplot as plt
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


strategies_full = {"bfs": "BFS", "dfs": "DFS",
                   "h": "Path heuristic", "nh": "Neighbor heuristic"}
violation_types = ["reach", "iso"]


def normalize_topo_violations(parsed_violations: dict) -> dict:
    violations = dict()

    for strat, strat_results in parsed_violations.items():
        normalized_violations = dict()
        last_iteration = 1
        last_num_violations = list(strat_results.values())[0]

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
        parsed_strategy_results = dict()

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

    for vio_type in violation_types:
        for strat_code, strat in strategies_full.items():
            try:
                strat_violations: list = read_violations_log(topo_name, vio_type, strat_code)
                all_violations[vio_type].update({strat: strat_violations})
            except FileNotFoundError:
                continue

    return all_violations


def read_violations_log(topo_name: str, vio_type: str, strat: str) -> dict:
    log_dir = "{}/{}".format(const.VIOLATIONS_DIR, topo_name)
    filename = "{}_violations_{}.log".format(vio_type, strat)
    filepath = "{}/{}".format(log_dir, filename)

    violations = dict()

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


def plot_topo_violations(topo_name: str, vio_type: str):
    raw_violations = read_topo_violations(topo_name)
    parsed_violations = parse_topo_violations(raw_violations[vio_type])
    print(json.dumps(parsed_violations, indent=4))
    normalized_violations = normalize_topo_violations(parsed_violations)
    print(json.dumps(normalized_violations, indent=4))
    make_violations_plot(normalized_violations)


def main():
    plot_topo_violations("ctree", "iso")


main()
