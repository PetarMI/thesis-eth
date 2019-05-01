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
