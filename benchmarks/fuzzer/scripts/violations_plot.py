import csv
import json
import matplotlib.pyplot as plt
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


strategies_full = {"bfs": "BFS", "dfs": "DFS",
                   "h": "Path heuristic", "nh": "Neighbor heuristic"}


def read_topo_violations(topo_name: str) -> dict:
    all_violations = dict()

    for strat_code, strat in strategies_full.items():
        try:
            strat_violations: list = read_run_violations(topo_name, strat_code)
            all_violations.update({strat: strat_violations})
        except FileNotFoundError:
            continue

    return all_violations


def read_run_violations(topo_name: str, strategy: str) -> list:
    """ Return list of ints """
    filepath = "{}/{}/violations_{}.log".format(const.LOG_DIR, topo_name, strategy)
    violations = []

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            violations.append(int(row[1]))

    return violations


def normalize_violations(violations: dict):
    num_iterations = []

    for v in violations.values():
        num_iterations.append(len(v))

    max_iterations = max(num_iterations)

    for s, v in violations.items():
        v.extend([v[-1]] * (max_iterations - len(v)))
        violations.update({s: v})

    return violations, max_iterations


def plot_violations(topo_name):
    violations = read_topo_violations(topo_name)

    # x_axis = list(range(x_range))

    fig, ax = plt.subplots()

    for s, v in violations.items():
        plt.plot(list(range(len(v))), v, label=s)

    plt.ylabel('Properties violated')
    plt.xlabel("Number of iterations")
    ax.set_title('Property violations comparison')
    plt.legend()

    plt.show()


def main():
    plot_violations("hiberniaus")


main()
