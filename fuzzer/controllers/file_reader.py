import csv
import json
from fuzzer.controllers import constants_controller as const


def read_topo() -> dict:
    with open(const.TOPO_FILE) as topo_file:
        topo = json.load(topo_file)

    return topo


def read_properties() -> dict:

    with open(const.PROPERTIES_FILE) as properties_file:
        properties = json.load(properties_file)

    return properties


def read_nat_ips() -> dict:
    matched_ips = const.IP_NAT_FILE
    return read_dev_csv(matched_ips)


def read_vm_info() -> dict:
    vm_file = const.VM_FILE
    return read_dev_csv(vm_file)


def read_dev_csv(filepath: str) -> dict:
    """ For per device configs:
        <device_name>,<old_val>,<new_val>"""
    iface_dict = {}

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            iface_dict.setdefault(row[0], {}).update({
                row[1]: row[2]
            })

    return iface_dict
