import numpy as np
import matplotlib.pyplot as plt
from benchmarks.simulator.scripts import log_reader as lr
from benchmarks.simulator.scripts import constants_bench as const


depl_metrics = ["dirs", "gencomp", "upload", "phynet", "setup", "download",
                "nat", "configs", "restart", "total"]


###############################################################################
# ######################## Parsing depl files #################################
###############################################################################
def parse_measurement(dir_path: str, instances: list):
    experiment_results = dict()

    for metric in depl_metrics:
        experiment_results.setdefault(metric, {"means": [],
                                               "stds": []})

    for instance in instances:
        instance_dir = "{}/{}".format(dir_path, instance)
        instance_runs: dict = get_instance_runs(instance_dir)
        instance_results: dict = parse_instance_metrics(instance_runs)

        for metric, value in instance_results.items():
            experiment_results[metric]["means"].append(value[0])
            experiment_results[metric]["stds"].append(value[1])

    return experiment_results


def parse_instance_metrics(instance_runs: dict) -> dict:
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


def get_instance_runs(instance_dir: str):
    """ Puts the depl_stats of all runs in a dict """
    all_depl_stats = dict()

    for idx in range(1, const.RUNS + 1):
        run_logs_dir = const.RUN_LOGS.format(idx)
        run_stats: dict = lr.read_run_depl_stats("{}/{}".format(instance_dir, run_logs_dir))

        all_depl_stats.update({idx: run_stats})

    return all_depl_stats


###############################################################################
# ######################$## Parsing ALL runs $#################################
###############################################################################
def parse_metric_ratios():
    runs: list = get_all_runs()
    metric_ratios = dict()
    avg_ratios = dict()
    std_ratios = dict()

    for metric in depl_metrics:
        metric_ratios.setdefault(metric, [])

    for run in runs:
        run_ratios: dict = parse_run_ratio(run)

        for metric, ratio in run_ratios.items():
            metric_ratios[metric].append(ratio)

    for metric, ratios in metric_ratios.items():
        avg_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)

        avg_ratios.update({metric: avg_ratio})
        std_ratios.update({metric: std_ratio})

    avg_ratios.pop("gencomp", None)
    avg_ratios.pop("total", None)

    return avg_ratios


def parse_run_ratio(run: dict) -> dict:
    run_ratios = dict()

    for metric, value in run.items():
        ratio = (100 * value) / run["total"]
        run_ratios.update({metric: ratio})

    return run_ratios


def get_all_runs() -> list:
    dir_path = const.TOPO_LOG_DIR
    instance_dirs = ["ctree", "hiberniaus", "bics", "iris", "columbus",
                     "oteglobe", "ion", "us_carrier"]

    all_runs = []

    for instance in instance_dirs:
        instance_dir = "{}/{}".format(dir_path, instance)
        instance_runs = get_instance_runs(instance_dir)

        all_runs.extend(instance_runs.values())

    return all_runs


class PlotOptimalVMs:
    @staticmethod
    def plot_optimal_vms(metric: str):
        dir_path = const.VM_LOGS_DIR
        instance_dirs = ["vm_3", "vm_5", "vm_8", "vm_10"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        total_means = ovms_results[metric]["means"]
        total_stds = ovms_results[metric]["stds"]

        ind = np.arange(4)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, total_means, width, yerr=total_stds,
                     capsize=2)

        plt.ylabel('Seconds')
        plt.xlabel('Number of routers per VM')
        plt.title('Overall deployment time')
        plt.xticks(ind, ('3', '5', '8', '10'))
        # plt.yticks(np.arange(200, 500, 100))
        # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

        plt.show()

    @staticmethod
    def plot_decreasing_metrics():
        dir_path = const.VM_LOGS_DIR
        instance_dirs = ["vm_3", "vm_5", "vm_8", "vm_10"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        upload_means = ovms_results["upload"]["means"]
        upload_stds = ovms_results["upload"]["stds"]
        download_means = ovms_results["download"]["means"]
        download_stds = ovms_results["download"]["stds"]

        ind = np.arange(4)  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2, upload_means, width, yerr=upload_stds,
                        label='Upload')
        rects2 = ax.bar(ind + width / 2, download_means, width, yerr=download_stds,
                        label='Download')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Seconds')
        ax.set_xlabel('Number of routers per VM')
        ax.set_title('Decreasing metrics')
        ax.set_xticks(ind)
        ax.set_xticklabels(('3', '5', '8', '10'))
        ax.legend()

        fig.tight_layout()

        plt.show()

    @staticmethod
    def plot_steady_metrics():
        dir_path = const.VM_LOGS_DIR
        instance_dirs = ["vm_3", "vm_5", "vm_8", "vm_10"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        phynet_means = ovms_results["phynet"]["means"]
        phynet_stds = ovms_results["phynet"]["stds"]
        restart_means = ovms_results["restart"]["means"]
        restart_stds = ovms_results["restart"]["stds"]

        ind = np.arange(4)  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2, phynet_means, width, yerr=phynet_stds,
                        label='Phynet')
        rects2 = ax.bar(ind + width / 2, restart_means, width, yerr=restart_stds,
                        label='Restart')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Seconds')
        ax.set_xlabel('Number of routers per VM')
        ax.set_title('Steady metrics')
        ax.set_xticks(ind)
        ax.set_xticklabels(('3', '5', '8', '10'))
        ax.legend()

        fig.tight_layout()

        plt.show()

    @staticmethod
    def plot_all_metrics():
        dir_path = const.VM_LOGS_DIR
        instance_dirs = ["vm_3", "vm_5", "vm_8", "vm_10"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        # growing
        setup_means = ovms_results["setup"]["means"]
        setup_stds = ovms_results["setup"]["stds"]
        # steady
        phynet_means = ovms_results["phynet"]["means"]
        phynet_stds = ovms_results["phynet"]["stds"]
        restart_means = ovms_results["restart"]["means"]
        restart_stds = ovms_results["restart"]["stds"]
        # decreasing
        upload_means = ovms_results["upload"]["means"]
        upload_stds = ovms_results["upload"]["stds"]
        download_means = ovms_results["download"]["means"]
        download_stds = ovms_results["download"]["stds"]

        ind = np.arange(4)  # the x locations for the groups
        width = 0.15  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - 0.3, setup_means, width, yerr=setup_stds,
                        label='L3 setup')
        rects2 = ax.bar(ind - 0.15, phynet_means, width, yerr=phynet_stds,
                        label='L2 setup')
        rects3 = ax.bar(ind, restart_means, width, yerr=restart_stds,
                        label='L3 config')
        rects4 = ax.bar(ind + 0.15, upload_means, width, yerr=upload_stds,
                        label='Upload')
        rects5 = ax.bar(ind + 0.3, download_means, width, yerr=download_stds,
                        label='Download')


        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Seconds')
        ax.set_xlabel('Number of routers per VM')
        #ax.set_title('All met')
        ax.set_xticks(ind)
        ax.set_xticklabels(('3', '5', '8', '10'))
        ax.legend()

        fig.tight_layout()

        plt.show()


class PlotTopoBenches:
    @staticmethod
    def plot_topos(metric: str):
        dir_path = const.TOPO_LOG_DIR
        instance_dirs = ["ctree", "hiberniaus", "bics", "iris", "columbus",
                         "oteglobe", "ion", "us_carrier"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        total_means = ovms_results[metric]["means"]
        total_stds = ovms_results[metric]["stds"]

        N = 8
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, total_means, width, yerr=total_stds, capsize=2)

        plt.ylabel('Seconds')
        plt.xlabel("Number of routers in topology")
        # plt.title('Deployment times of different topologies')
        plt.xticks(ind, ('11/5', '22/6', '33/10', '51/10', '70/14', '93/15', '125/19', '156/21'))

        plt.show()

    @staticmethod
    def plot_metric_ratios():
        metric_ratios = parse_metric_ratios()

        metrics = ["Setup L3 containers", "L2 Docker Compose", "Others"]
        ratios = [metric_ratios["setup"], metric_ratios["phynet"],
                  100 - metric_ratios["setup"] - metric_ratios["phynet"]]

        fig1, ax1 = plt.subplots()
        patches, texts, autotexts = ax1.pie(ratios, labels=metrics, autopct='%1.1f%%', textprops={'fontsize': 14}, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        texts[0].set_fontsize(20)
        texts[1].set_fontsize(20)
        texts[2].set_fontsize(20)

        plt.show()

    @staticmethod
    def plot_topos_important_metrics():
        dir_path = const.TOPO_LOG_DIR
        instance_dirs = ["ctree", "hiberniaus", "bics", "iris", "columbus",
                         "oteglobe", "ion", "us_carrier"]

        ovms_results: dict = parse_measurement(dir_path, instance_dirs)
        phynet_means = ovms_results["phynet"]["means"]
        phynet_stds = ovms_results["phynet"]["stds"]
        setup_means = ovms_results["setup"]["means"]
        setup_stds = ovms_results["setup"]["stds"]

        ind = np.arange(8)  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind - width / 2, phynet_means, width, yerr=phynet_stds,
                        label='L2 Docker Compose', capsize=2)
        rects2 = ax.bar(ind + width / 2, setup_means, width, yerr=setup_stds,
                        label='Setup L3 containers', capsize=2)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        plt.ylabel('Seconds')
        plt.xlabel("Number of routers in topology")
        # ax.set_title('Biggest metrics')
        ax.set_xticks(ind)
        plt.xticks(ind, ('11/5', '22/6', '33/10', '51/10', '70/14', '93/15', '125/19', '156/21'))
        ax.legend(loc=2)

        fig.tight_layout()

        plt.show()


if __name__ == "__main__":
    ovms = PlotOptimalVMs()
    tb = PlotTopoBenches()

    #ovms.plot_optimal_vms("total")
    # ovms.plot_optimal_vms("setup")
    # ovms.plot_decreasing_metrics()
    # ovms.plot_steady_metrics()
    # ovms.plot_all_metrics()

    # tb.plot_topos("total")
    # tb.plot_metric_ratios()
    tb.plot_topos_important_metrics()
