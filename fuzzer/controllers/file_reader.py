import csv
import ipaddress
import json
import constants_controller as const


def read_topo() -> dict:
    with open(const.TOPO_FILE) as topo_file:
        topo = json.load(topo_file)

    return topo


def read_properties(prop_type: str) -> dict:

    with open(const.PROPERTIES_FILE) as properties_file:
        properties = json.load(properties_file)

    return properties[prop_type]


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
