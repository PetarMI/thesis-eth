""" Baseline strategy planner

This script allows generates how the fuzzer is going to traverse the
search space in a BFS/DFS manner.

The input to the script is the max depth K that we are checking.

This file is imported as a module inside the Statespace class
Public functions:

    * bfs - Generates a BFS search strategy
    * dfs - Generates a DFS search strategy
"""

from itertools import combinations


# @Tested
def bfs(depth: int, nets: list):
    """ Makes a search plan based on BFS algo """
    search_plan = []

    for k in range(0, depth + 1):
        depth_k_search = list(combinations(nets, k))
        search_plan.extend(depth_k_search)

    return search_plan


# @Tested
def dfs(max_depth: int, nets: list) -> list:
    """ Makes a search plan based on DFS algo """
    empty_state = ()
    statespace = dfs_aux(empty_state, nets, 1, max_depth)
    statespace.insert(0, empty_state)

    return statespace


# @Tested as part of calling function
def dfs_aux(parent_state: tuple, nets: list, depth: int, max_depth: int) -> list:
    search_plan = []

    if not nets:
        return search_plan

    if depth == max_depth:
        for link in nets:
            search_plan.append(parent_state + (link,))

        return search_plan

    for idx, link in enumerate(nets, start=1):
        top_state: tuple = parent_state + (link,)
        search_plan.append(top_state)

        child_plan = dfs_aux(top_state, nets[idx:], depth + 1, max_depth)
        search_plan.extend(child_plan)

    return search_plan
