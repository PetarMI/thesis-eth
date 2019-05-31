""" Fuzzer file reader

Implements functions for reading all data which is generated
during deployment and later used by the fuzzer.

How to use: * Only the FuzzData class should read raw data using
            the file reader as it provides a wrapper.
            * Exception is the Property parser which can call ONLY
            the functions related to reading property data
"""

import csv
import ipaddress
import json
from fuzzer.common import constants_fuzzer as const


def read_topo() -> dict:
    with open(const.TOPO_FILE) as topo_file:
        topo = json.load(topo_file)

    return topo


def read_nat_ips() -> dict:
    """ Return a dict representation of the nat-ed IPs as ipaddress types """
    nat_ips_file = const.IP_NAT_FILE

    nat_ips = {}

    with open(nat_ips_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            casted_orig_ip = ipaddress.IPv4Interface(row[1])
            casted_sim_ip = ipaddress.IPv4Interface(row[2])

            nat_ips.setdefault(row[0], {}).update({
                casted_orig_ip: casted_sim_ip
            })

    return nat_ips


def read_vm_info() -> dict:
    vm_file = const.VM_FILE
    vm_dict = {}

    with open(vm_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            vm_dict.setdefault(row[0], {}).update({
                "ip": row[1],
                "role": row[2]
            })

    return vm_dict


def read_sim_networks(swap=False) -> dict:
    """ Reads a file with two columns into a dictionary

    :param order: False to swap column key-value order
    :return: Network names to IPs if `order` and vice-versa otherwise
    """
    networks_file = const.NETS_FILE

    networks = {}

    with open(networks_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            dict_key, dict_val = swap_order(row[0], row[1], swap)

            networks.update({
                dict_key: dict_val
            })

    return networks


def read_sim_ifaces() -> dict:
    sim_ifaces_file = const.SIM_IFACES_FILE

    iface_dict = {}

    with open(sim_ifaces_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            iface_dict.setdefault(row[0], {}).update({
                row[2]: row[1]
            })

    return iface_dict


def read_properties(prop_type: str) -> dict:
    with open(const.PROPERTIES_FILE) as properties_file:
        properties = json.load(properties_file)

    return properties[prop_type]


def read_reachability_properties() -> list:
    prop_file = const.PARSED_PROPS_FILE

    with open(prop_file, 'r') as json_file:
        properties = json.load(json_file)

    return properties


def read_ping_file(idx: int) -> str:
    ping_file = const.PING_FILE.format(idx)
    filepath = "{}/{}".format(const.PING_LOGS_DIR, ping_file)

    with open(filepath, 'r') as txt_file:
        ping_data = txt_file.read()

    return ping_data


def swap_order(val_a, val_b, swap: bool):
    """ Return the two vals in the specified order """
    if swap:
        return val_b, val_a
    else:
        return val_a, val_b
