import os
from argparse import ArgumentParser
import nat_subnets
import nat_ifaces
import nat_writer as nw
import constants as const


class NatController:

    def __init__(self, topo_name: str):
        self.topo_name = topo_name
        self.output_dir = "{}/{}{}".format(const.DPL_FILES_DIR,
                                           self.topo_name, const.NAT_FILES)

    def nat_matching(self):
        """ Main function that does NAT on all components:
            - subnets / interfaces / IP addresses

        :return: writes the results to files that are processed by bash scripts
        """
        print("Matching subnets")
        matched_subnets = nat_subnets.perform_match(self.topo_name)

        print("Matching interfaces and IP addresses")
        ifaces, ips = nat_ifaces.perform_match(self.topo_name, matched_subnets)

        print("Writing matches to files")
        self.write_matched_files(matched_subnets, ifaces, ips)

    def write_matched_files(self, subnets: dict, ifaces: dict, ips: dict):
        os.makedirs(self.output_dir, exist_ok=True)
        nw.write_subnets(self.output_dir, subnets)
        nw.write_ifaces(self.output_dir, ifaces)
        nw.write_ips(self.output_dir, ips)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.topology

    nat_contr = NatController(topo_name)
    nat_contr.nat_matching()
