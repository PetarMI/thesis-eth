import csv
import json
from fuzzer.common import constants_fuzzer as const


def write_search_plan(search_plan: list):
    output_file = const.SEARCH_PLAN_LOG

    with open(output_file, 'w+') as log_file:
        for state in search_plan:
            log_file.write("{}\n".format(state))


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
            log_file.write("\tExtra Info: {}\n".format(ver_res.get("info", None)))
            log_file.write("===========================\n")


def track_reach_progress(reach_iterations, property_failures):
    filepath: str = const.REACH_VIOLATIONS_LOG
    write_violations_progress(filepath, reach_iterations, property_failures)


def track_iso_progress(iso_iterations, property_failures):
    filepath: str = const.ISO_VIOLATIONS_LOG
    write_violations_progress(filepath, iso_iterations, property_failures)


def write_violations_progress(filepath: str, iterations, prop_failures: dict):
    failed_props = ",".join(str(x) for x in prop_failures.keys())

    with open(filepath, mode='a+') as log_file:
        log_file.write("{}:{}\n".format(iterations, failed_props))
