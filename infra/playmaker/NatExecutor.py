import csv
from argparse import ArgumentParser
import constants as const
import topo_parser as tp


class NatExecutor:

    def __init__(self, topo_name: str):
        self.topo_name = topo_name

    def execute_nat(self):
        orig_subnets = self.parse_orig_subnets()
        sim_subnets = self.parse_sim_subnets()

        subnet_sanity_check(orig_subnets, sim_subnets)
        subnets = match_subnets(orig_subnets, sim_subnets)
        print(subnets)

    def parse_orig_subnets(self) -> dict:
        topo_file = "{0}/{1}/{1}.topo".format(const.TOPO_DIR, self.topo_name)
        topo_nets: list = tp.find_nets(tp.import_topo(topo_file))
        subnets = {}

        for net in topo_nets:
            sim_name = self.update_net_name(tp.safe_get(net, "name"))
            subnets.update({
                sim_name: tp.safe_get(net, "subnet")
            })

        return subnets

    def parse_sim_subnets(self) -> dict:
        networks_log_file = "{}/{}/{}".format(const.NAT_DIR, self.topo_name,
                                              const.NET_LOG_FILE)
        subnets = {}

        with open(networks_log_file, 'r') as sim_nets_file:
            csv_reader = csv.reader(sim_nets_file, delimiter=',')

            for row in csv_reader:
                subnets.update({
                    row[0]: row[1]
                })

        return subnets

    def update_net_name(self, orig_net_name: str) -> str:
        return "{}-{}".format(self.topo_name, orig_net_name)


def match_subnets(orig_subnets: dict, sim_subnets: dict) -> dict:
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


# TODO implement sanity check
def subnet_sanity_check(orig_subnets: dict, sim_subnets: dict) -> bool:
    return True


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.topology

    nat_exec = NatExecutor(topo_name)
    nat_exec.execute_nat()
