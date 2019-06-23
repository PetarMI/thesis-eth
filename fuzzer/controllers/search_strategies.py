""" BFS search strategy planner

This script allows generates how the fuzzer is going to traverse the
search space in a BFS/DFS manner.

The input to the script is the max depth K that we are checking.

This file is imported as a module inside the Statespace class
Public functions:

    * bfs - Generates a BFS search strategy
    * dfs - Generates a DFS search strategy
"""

from itertools import combinations
from collections import OrderedDict


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


# @Tested
def heuristic(max_depth: int, links: list, property_links: list) -> list:
    """ Makes a search plan based on a heuristic """
    heuristic_subplan: list = dfs(max_depth, property_links)
    full_dfs_plan: list = dfs(max_depth, links)

    pre_validate_heuristic_gen(heuristic_subplan, full_dfs_plan)
    heuristic_plan: list = gen_full_heuristic(heuristic_subplan, full_dfs_plan)
    post_validate_heuristic_gen(heuristic_plan, full_dfs_plan)

    return heuristic_plan


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


# @Tested
def gen_full_heuristic(subplan: list, full_plan: list) -> list:
    lookup_subplan = OrderedDict.fromkeys(subplan)
    heuristic_plan = subplan.copy()

    for state in full_plan:
        if state not in lookup_subplan:
            heuristic_plan.append(state)

    return heuristic_plan


# @Tested
def pre_validate_heuristic_gen(heuristic_plan: list, full_plan: list):
    if not heuristic_plan:
        raise ValueError("Empty heuristic plan")

    if not set(heuristic_plan).issubset(set(full_plan)):
        raise ValueError("Heuristic plan is not subset of the full plan")


# @Tested
def post_validate_heuristic_gen(heuristic_plan: list, dfs_plan: list):
    if len(heuristic_plan) != len(dfs_plan):
        raise ValueError("Heuristic plan expected length - {} vs real {}".format(
            len(heuristic_plan), len(dfs_plan)
        ))
