from argparse import ArgumentParser
import constants as const

class NatExecutor:

    def __init__(self, topo: str):
        self.topo = topo

    def match_subnets(self) -> dict:
        subnets = self.fill_orig_subnets()

    def fill_orig_subnets(self):
        topo_file = "{}/{}/toy."

    def update_net_name(self, orig_net_name: str) -> str:
        return "{}-{}".format(self.topo, orig_net_name)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-t", "--topology", dest="topology",
                        help="Topology file to be used for setup")
    args = parser.parse_args()

    topo_name: str = args.topology

    nat_exec = NatExecutor(topo_name)
    # print(nat_exec.update_net_name(topo_name))
