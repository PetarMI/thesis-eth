import csv
import constants as const
import json


def read_orig_ifaces(topo: str) -> dict:
    o_ifaces_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                        const.NAT_FILES, const.ORIG_IFACES_FILE)

    o_ifaces = read_ifaces_csv(o_ifaces_file)
    return o_ifaces


def read_sim_ifaces(topo: str) -> dict:
    s_ifaces_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                        const.NAT_FILES, const.SIM_IFACES_FILE)

    s_ifaces = read_ifaces_csv(s_ifaces_file)
    return s_ifaces


def read_sim_subnets(topo: str) -> dict:
    subnets_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                       const.LOGS_DIR, const.NET_LOG_FILE)
    sim_subnets = read_simple_csv(subnets_file)

    return sim_subnets


def read_matched_subnets(topo: str) -> dict:
    subnets_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                       const.NAT_FILES, const.SUBNETS_FILE)
    matched_subnets = read_simple_csv(subnets_file)

    return matched_subnets


def read_ifaces_csv(filepath: str) -> dict:
    iface_dict = {}

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            iface_dict.setdefault(row[0], {}).update({
                row[1]: row[2]
            })

    return iface_dict


def read_simple_csv(filepath: str):
    simple_dict = {}

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            simple_dict.update({
                row[0]: row[1]
            })

    return simple_dict

print(json.dumps(read_orig_ifaces("toy"), indent=4))
print(json.dumps(read_sim_ifaces("toy"), indent=4))
