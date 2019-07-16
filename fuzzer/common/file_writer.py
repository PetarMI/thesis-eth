import csv
import json
from fuzzer.common import constants_fuzzer as const


def write_reach_instr(properties: dict):
    output_file = const.REACH_PROPS_FILE

    with open(output_file, mode='w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for prop in properties.values():
            writer.writerow([prop["vm_ip"], prop["container_name"],
                             prop["dest_sim_ip"]])


def write_reach_properties(reach_properties: dict):
    output_file = const.PARSED_PROPS_FILE
    prop_list = list(reach_properties.values())

    with open(output_file, 'w+') as json_file:
        json.dump(prop_list, json_file, indent=4)


def write_iso_properties(iso_properties: dict):
    output_file = const.PARSED_ISO_FILE
    prop_list = list(iso_properties.values())

    with open(output_file, 'w+') as json_file:
        json.dump(prop_list, json_file, indent=4)


def write_state_failures(state: tuple, property_violations: dict):
    output_file = const.FAILURES_LOG

    with open(output_file, mode='a+') as log_file:
        log_file.write("State: {}\n".format(state))

        for pid, ver_res in property_violations.items():
            log_file.write("\tFailed property {}\n".format(pid))
            log_file.write("\tDescription: {}\n".format(ver_res["desc"]))
            log_file.write("\tExtra Info: {}\n".format(ver_res["info"]))
            log_file.write("===========================\n")
