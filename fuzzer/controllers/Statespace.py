""" Search strategy planner

This script is the entry point of the search strategy planning.

* Calls the correct search strategy function so it can be thought of
  as a dispatcher.

Public functions:
    * get_search_plan - returns search plan generated by the specified algorithm
    * get_fuzzing_stats - stats about number of scenarios at each depth
"""

from scipy.special import comb
from fuzzer.controllers import search_strategies as strategies


class Statespace:
    def __init__(self, depth: int, nets: list):
        self.depth = depth
        self.nets = nets
        self.verify_input()

    def get_search_plan(self, algo: str) -> list:
        """ Function that calls the correct search algorithm """
        if algo == "bfs":
            search_plan = strategies.bfs(self.depth, self.nets)
        elif algo == "dfs":
            search_plan = strategies.dfs(self.depth, self.nets)
        else:
            raise ValueError("Unknown search algorithm {}".format(algo))

        return search_plan

    # @Tested
    def get_fuzzing_stats(self) -> dict:
        """ Get info about the possible failures for each depth """
        stats = {}
        total = 0
        N = len(self.nets)

        for k in range(0, self.depth + 1):
            num_combs = comb(N, k, exact=True)
            depth_key = "depth{}".format(k)
            stats.update({depth_key: num_combs})
            total += num_combs

        stats.update({"total": total})

        return stats

    # @Tested
    def verify_input(self):
        """ Function that collects all checks on the class input """
        verify_depth(self.depth, self.nets)


# @Tested composite
def verify_depth(depth: int, nets: list):
    """ Verify depth is not greater than the number of elements in the list
    In that case the underlying combinations algorithm would just give
    all combinations as if (depth == len(nets)) but we choose to raise
    an exception as this is likely indicative of an error somewhere
    """
    if depth > len(nets):
        raise ValueError("Depth is higher than number of nets")
