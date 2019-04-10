import csv
import constants as const


def read_orig_ifaces(topo: str) -> dict:
    o_ifaces_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                        const.NAT_FILES, const.ORIG_IFACES_FILE)


def read_sim_ifaces(topo: str) -> dict:
    s_ifaces_file = "{}/{}{}/{}".format(const.DPL_FILES_DIR, topo,
                                        const.NAT_FILES, const.SIM_IFACES_FILE)
    return {}


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


def read_simple_csv(filepath: str):
    simple_dict = {}

    with open(filepath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            simple_dict.update({
                row[0]: row[1]
            })

    return simple_dict
