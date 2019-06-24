from collections import OrderedDict
from fuzzer.strategies import baseline_strategies as base


# @Tested
def heuristic(max_depth: int, links: list, property_links: list) -> list:
    """ Makes a search plan based on a heuristic """
    heuristic_subplan: list = base.dfs(max_depth, property_links)
    full_dfs_plan: list = base.dfs(max_depth, links)

    pre_validate_heuristic_gen(heuristic_subplan, full_dfs_plan)
    heuristic_plan: list = gen_full_heuristic(heuristic_subplan, full_dfs_plan)
    post_validate_heuristic_gen(heuristic_plan, full_dfs_plan)

    return heuristic_plan


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


# def exec_next_hop_find(prop: dict) -> str:
#     """ Execute the next hop finding script and return a
#     comma separated string of IP addresses without a netmask """
#     result = subprocess.run([const.FIB_SH, prop["vm_ip"], prop["container_name"],
#                              prop["dest_sim_net"]], stdout=subprocess.PIPE)
#     next_hops: str = result.stdout.decode('utf-8')
#
#     return next_hops
#
#
# def parse_hop_links(links: str) -> :
# def find_property_links(properties: list) -> list:
#     """ Find the links associated with each property """
#     raise ValueError("Not implemented")