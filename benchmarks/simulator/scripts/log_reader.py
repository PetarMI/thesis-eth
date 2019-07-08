import csv
from benchmarks.simulator.scripts import constants_bench as const


def read_run_depl_stats(dir_path: str):
    filepath = "{}/{}".format(dir_path, const.DEPL_STATS)
    simple_dict = {}

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        total = 0

        for row in csv_reader:
            total += int(row[1])

            simple_dict.update({
                row[0]: int(row[1])
            })

        simple_dict.update({"total": total})

    return simple_dict
