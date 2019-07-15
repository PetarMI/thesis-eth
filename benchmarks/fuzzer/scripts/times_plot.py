import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


strategies_full = {"bfs": "BFS", "dfs": "DFS",
                   "h": "Path heuristic", "nh": "Neighbor heuristic"}

topologies = ["ctree", "hiberniaus"]


def parse_transition_times():
    all_times = dict()
    all_times.update({"drop": []})
    all_times.update({"restore": []})

    for topo_name in topologies:
        for strat_code, strat in strategies_full.items():
            try:
                run_times: dict = read_trans_run_times(topo_name, strat_code)
                all_times["drop"].extend(run_times["drop"])
                all_times["restore"].extend(run_times["restore"])
            except FileNotFoundError:
                continue

    return all_times


def read_trans_run_times(topo_name: str, strategy: str) -> dict:
    filepath = "{}/{}/run_{}.log".format(const.LOG_DIR, topo_name, strategy)

    times = dict()
    times.update({"drop": []})
    times.update({"restore": []})

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        next(csv_reader)

        for row in csv_reader:
            times["drop"].append(float(row[0]))
            times["restore"].append(float(row[1]))

    return times


def parse_convergence_times():
    all_times = dict()
    all_times.update({"neighbors": []})
    all_times.update({"routes": []})

    for topo_name in topologies:
        try:
            conv_run_times: dict = read_topo_conv_times(topo_name)
            all_times["neighbors"].extend(conv_run_times["neighbors"])
            all_times["routes"].extend(conv_run_times["routes"])
        except FileNotFoundError:
            continue

    return all_times


def read_topo_conv_times(topo_name: str):
    filepath = "{}/{}/conv_stats.log".format(const.LOG_DIR, topo_name)

    times = dict()
    times.update({"neighbors": []})
    times.update({"routes": []})

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            times[row[0]].append(int(row[1]))

    return times


def parse_verification_times() -> dict:
    ver_times: dict = read_verification_times()
    parsed_ver = {"xaxis": [], "means": [], "errs": []}

    for nprops, times in ver_times.items():
        parsed_ver["xaxis"].append(nprops)
        parsed_ver["means"].append(np.mean(times))
        parsed_ver["errs"].append(np.std(times))

    return parsed_ver


def read_verification_times() -> dict:
    filepath = "{}/verification.log".format(const.LOG_DIR)

    times = dict()

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            times.setdefault(int(row[0]), []).append(float(row[1]))

    return times


def parse_fuzz_ops() -> list:
    """ Return list of ints """
    filepath = "{}/hiberniaus/fuzz_ops.log".format(const.LOG_DIR)
    times = []

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            times.append(float(row[0]))

    return times


def plot_transition_times():
    fuzz_ops_times = parse_fuzz_ops()
    trans_times = parse_transition_times()
    conv_times = parse_convergence_times()

    mean_times = [np.mean(fuzz_ops_times), np.mean(trans_times["drop"]),
                  np.mean(trans_times["restore"]), np.mean(conv_times["neighbors"]),
                  np.mean(conv_times["routes"])]
    std_err = [np.std(fuzz_ops_times), np.std(trans_times["drop"]),
               np.std(trans_times["restore"]), np.std(conv_times["neighbors"]),
               np.std(conv_times["routes"])]

    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, mean_times, width, yerr=std_err, capsize=3)

    plt.ylabel('Seconds')
    plt.xlabel("Metrics")
    plt.title('Times spent during state transition')
    plt.xticks(ind, ("Fuzz Ops", "Link Drop", "Link Restore", "Neighbor\nadjacency", "Route\nconvergence"))

    plt.show()


def plot_ver_times():
    ver_times = parse_verification_times()

    plt.errorbar(ver_times["xaxis"], ver_times["means"], yerr=ver_times["errs"],
                 fmt='-o', ecolor='red', markersize=5, capsize=2)
    plt.ylabel('Seconds')
    plt.xlabel("Properties")
    plt.title('Reachability Verification')

    plt.show()


def main():
    # plot_transition_times()
    plot_ver_times()

main()
