import csv
import constants_controller as const


def write_reach_file(properties: list):
    output_file = const.REACH_FILE

    with open(output_file, mode='w+') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for prop in properties:
            writer.writerow([prop["vm_ip"], prop["container_name"],
                             prop["dest_ip"]])
