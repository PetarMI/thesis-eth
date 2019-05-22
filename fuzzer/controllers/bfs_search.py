""" BFS search strategy planner

This script allows generates how the fuzzer is going to traverse the
search space in a BFS manner. It will guide the fuzzer to first check all
network space where there is 1 failed link, then all spaces with 2 and so on.

The input to the script is the depth K that we are checking.

This script requires no weird modules to be installed in the environment.

This file can also be imported as a module or called on its own.
Public functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

from itertools import combinations
from argparse import ArgumentParser
from fuzzer.common import file_reader as fr


class BFSPlanner:

    def __init__(self, depth: int, nets: list):
        self.depth = depth
        self.nets = nets
        self.search_plan = []

    def bfs(self) -> list:
        last_level_count = 0

        for k in range(1, self.depth):
            depth_k_search = self.search_level(k, last_level_count)
            last_level_count = len(depth_k_search)
            self.search_plan.extend(depth_k_search)

        return self.search_plan

    def search_level(self, k: int, last_level_count: int) -> list:
        return []


def bfs(depth: int, nets: list):
    search_plan = []

    for k in range(1, depth + 1):
        depth_k_search = list(combinations(nets, k))
        search_plan.extend(depth_k_search)

    return search_plan


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", dest="depth",
                        help="The max depth we are checking for failed links")
    args = parser.parse_args()

    if args.depth:
        search_depth: int = int(args.depth)
        input = ['a', 'b', 'c', 'd']
        bfs(search_depth, input)
    else:
        raise ValueError("Forgot to specify search depth via -d")
