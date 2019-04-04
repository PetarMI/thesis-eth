import csv
from argparse import ArgumentParser
import nat_subnets


class NatExecutor:

    def __init__(self, topo_name: str):
        self.topo_name = topo_name

    def execute_nat(self):
        subnets = nat_subnets.perform_nat(self.topo_name)
        print(subnets)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.topology

    nat_exec = NatExecutor(topo_name)
    nat_exec.execute_nat()
