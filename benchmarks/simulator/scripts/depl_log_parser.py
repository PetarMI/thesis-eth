import numpy as np
# import matplotlib.pyplot as plt
from benchmarks.simulator.scripts import log_reader as lr
from benchmarks.simulator.scripts import constants_bench as const


depl_metrics = ["dirs", "gencomp", "upload", "phynet", "setup", "download",
                "nat", "configs", "restart"]


def parse_instance_depl_stats(instance_runs: dict) -> dict:
    instance_results = dict()

    for metric in depl_metrics:
        metric_results = parse_depl_metric(instance_runs, metric)
        instance_results.update({metric: metric_results})

    return instance_results


def parse_depl_metric(runs: dict, metric: str):
    metric_results = []

    for run in runs.values():
        metric_results.append(run[metric])

    metric_avg = np.mean(metric_results)
    metric_std = np.std(metric_results)

    return (metric_avg, metric_std)


def get_instance_runs_depl_stats(instance_dir: str):
    """ Puts the depl_stats of all runs in a dict """
    all_depl_stats = dict()

    for idx in range(1, const.RUNS + 1):
        run_logs_dir = const.RUN_LOGS.format(idx)
        run_stats: dict = lr.read_run_depl_stats("{}/{}".format(instance_dir, run_logs_dir))

        all_depl_stats.update({idx: run_stats})

    return all_depl_stats


def main():
    instances = ["vm_3", "vm_5", "vm_8", "vm_10"]
    parse_instances(instances)


if __name__ == "__main__":
    main()
