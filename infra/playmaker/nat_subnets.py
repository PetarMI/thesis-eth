import csv
import constants as const
import topo_parser as tp


def match_subnets(topo_name: str) -> dict:
    """ Main function of subnet matching functionality """

    # declare paths used during subnet matching
    topo_file = "{0}/{1}/{1}.topo".format(const.TOPO_DIR, topo_name)
    topo_nets: list = tp.find_nets(tp.import_topo(topo_file))

    sim_subnet_log = "{}/{}/{}/{}".format(const.DPL_FILES_DIR, topo_name,
                                          const.LOGS_DIR, const.NET_LOG_FILE)

    # perform matching
    orig_subnets = parse_orig_subnets(topo_name, topo_nets)
    sim_subnets = parse_sim_subnets(sim_subnet_log)

    subnets = match_addresses(orig_subnets, sim_subnets)

    return subnets


def parse_orig_subnets(topo_name: str, topo_nets: list) -> dict:
    subnets = {}

    for net in topo_nets:
        sim_name = update_net_name(topo_name, tp.safe_get(net, "name"))
        subnets.update({
            sim_name: tp.safe_get(net, "subnet")
        })

    return subnets


def parse_sim_subnets(sim_subnet_log: str) -> dict:
    subnets = {}

    with open(sim_subnet_log, 'r') as sim_nets_file:
        csv_reader = csv.reader(sim_nets_file, delimiter=',')

        for row in csv_reader:
            subnets.update({
                row[0]: row[1]
            })

    return subnets


def match_addresses(orig_subnets: dict, sim_subnets: dict) -> dict:
    subnets = {}

    for net_name, o_subnet in orig_subnets.items():
        s_subnet = tp.safe_get(sim_subnets, net_name)

        subnets.update({
            net_name: {
                "subnet": o_subnet,
                "sim_subnet": s_subnet
            }
        })

    return subnets


def update_net_name(topo_name, orig_net_name: str) -> str:
    return "{}-{}".format(topo_name, orig_net_name)


# TODO implement sanity check
def subnet_sanity_check(orig_subnets: dict, sim_subnets: dict) -> bool:
    return True
