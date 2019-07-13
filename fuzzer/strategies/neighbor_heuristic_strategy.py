from termcolor import colored as clr
from collections import OrderedDict
from fuzzer.common.FuzzData import FuzzData
from fuzzer.strategies import baseline_strategies as base


def heuristic(max_depth: int, properties: dict, fuzz_data: FuzzData):
    """ Makes a search plan based on a heuristic """
    ospf_links = fuzz_data.get_ospf_networks()

    heuristic_links: list = find_heuristic_links(properties, max_depth, fuzz_data)
    pretty_print_property_links(heuristic_links)

    heuristic_subplan: list = gen_heuristic_subplan(max_depth, heuristic_links)
    heuristic_plan: list = gen_full_plan(max_depth, heuristic_subplan, ospf_links)

    return heuristic_plan


# @Tested (one test)
def gen_full_plan(max_depth: int, heuristic_subplan: list, links: list) -> list:
    sorted_links = sorted(links)
    full_dfs_plan: list = base.dfs(max_depth, sorted_links)

    pre_validate_heuristic_gen(heuristic_subplan, full_dfs_plan)
    heuristic_plan: list = union_plans(heuristic_subplan, full_dfs_plan)
    post_validate_heuristic_gen(heuristic_plan, full_dfs_plan)

    return heuristic_plan


# @Tested (one test)
def gen_heuristic_subplan(max_depth: int, heuristic_links: list):
    heuristic_plan = []

    for prop_links in heuristic_links:
        prop_links.sort()
        prop_plan: list = base.dfs(max_depth, prop_links)
        heuristic_plan = union_plans(heuristic_plan, prop_plan)

    return heuristic_plan


# @Tested
def union_plans(subplan: list, full_plan: list) -> list:
    """ Combines the two plans by first adding states from the first one
    and then states from the second one which are non-overlapping.

    WARNING: plans must be sorted in the same order
    """
    lookup_subplan = OrderedDict.fromkeys(subplan)
    heuristic_plan = subplan.copy()

    for state in full_plan:
        if state not in lookup_subplan:
            heuristic_plan.append(state)

    return heuristic_plan


def find_heuristic_links(properties: dict, max_depth, fuzz_data: FuzzData) -> list:
    links = []
    topo_name = fuzz_data.get_topo_name()
    topo_containers = fuzz_data.get_topo_containers()

    for prop in properties.values():
        prop_links = set([])
        src_container = prop["container_name"].split("-")[1]

        src_links = find_container_links(src_container, topo_containers, topo_name)

        if len(src_links) > max_depth:
            links.append([])
            continue
        else:
            prop_links.update(src_links)

        for src_link in src_links:
            neighbor_name = get_neighbor_name(src_link, src_container)
            neighbor_links = find_container_links(neighbor_name, topo_containers, topo_name)

            if len(neighbor_links) >= max_depth:
                continue
            else:
                prop_links.update(neighbor_links)

        links.append(list(prop_links))

    return links


def find_container_links(cont_name: str, containers: list, topo_name) -> list:
    container_links = []

    container = find_container(cont_name, containers)

    for iface in container["interfaces"]:
        if not iface["ipaddr"].startswith("100."):
            container_links.append("{}-{}".format(topo_name, iface["network"]))

    return container_links


def find_container(c_name: str, containers: list) -> dict:
    for container in containers:
        if container["name"] == c_name:
            return container

    raise ValueError("Container {} not dound in topo file".format(c_name))


def get_neighbor_name(link: str, neighbor: str) -> str:
    parts = link.split("-")

    for dev in parts[2:]:
        if dev != neighbor:
            return dev

    raise ValueError("No neighbor of {} on link {}".format(neighbor, link))


def pretty_print_property_links(heuristic_links: list):
    print(clr("## Heuristic property links", 'magenta', attrs=['bold']))

    for idx, prop_links in enumerate(heuristic_links, start=1):
        print("Property {}: {}".format(idx, prop_links))


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
