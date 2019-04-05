import csv
import os
from argparse import ArgumentParser
import nat_subnets
import topo_parser as tp
import constants as const


class NatExecutor:

    def __init__(self, topo_name: str):
        self.topo_name = topo_name
        self.output_dir = "{}/{}{}".format(const.DPL_FILES_DIR,
                                           self.topo_name, const.NAT_FILES)

    def execute_nat(self):
        subnets = nat_subnets.perform_nat(self.topo_name)

        os.makedirs(self.output_dir, exist_ok=True)
        self.write_subnets(subnets)

    def write_subnets(self, subnets: dict):
        subnets_file = "{}/{}".format(self.output_dir, const.SUBNETS_FILE)

        with open(subnets_file, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

            for s in subnets.values():
                writer.writerow([tp.safe_get(s, "subnet"),
                                 tp.safe_get(s, "sim_subnet")])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.topology

    nat_exec = NatExecutor(topo_name)
    nat_exec.execute_nat()
