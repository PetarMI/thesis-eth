import csv
import json
from fuzzer.common import constants_fuzzer as const


def write_reach_instr(properties: list):
    output_file = const.REACH_PROPS_FILE

    with open(output_file, mode='w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for prop in properties:
            writer.writerow([prop["vm_ip"], prop["container_name"],
                             prop["dest_sim_ip"]])


def write_parsed_properties(properties: list):
    output_file = const.PARSED_PROPS_FILE

    with open(output_file, 'w+') as json_file:
        json.dump(properties, json_file, indent=4)


def write_state_failures(failures: list):
    output_file = const.FAILURES_LOG

    with open(output_file, mode='a+') as log_file:
        for f in failures:
            log_file.write("Failed property {}\n".format(f["pid"]))
            log_file.write("\tState: {}\n".format(f["state"]))
            log_file.write("\tDescription: {}\n".format(f["desc"]))
            log_file.write("===========================\n")
