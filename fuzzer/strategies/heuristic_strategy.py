import ipaddress
import subprocess
from collections import OrderedDict
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData
from fuzzer.strategies import baseline_strategies as base


# @Tested
def heuristic(max_depth: int, links: list, properties: list, fuzz_data) -> list:
    """ Makes a search plan based on a heuristic """
    heuristic_links: list = find_path_links(properties, fuzz_data)

    for prop in heuristic_links:
        print(prop)

    # full_dfs_plan: list = base.dfs(max_depth, links)

    # pre_validate_heuristic_gen(heuristic_subplan, full_dfs_plan)
    # heuristic_plan: list = union_plans(heuristic_subplan, full_dfs_plan)
    # post_validate_heuristic_gen(heuristic_plan, full_dfs_plan)

    return []


# @Tested
def union_plans(subplan: list, full_plan: list) -> list:
    lookup_subplan = OrderedDict.fromkeys(subplan)
    heuristic_plan = subplan.copy()

    for state in full_plan:
        if state not in lookup_subplan:
            heuristic_plan.append(state)

    return heuristic_plan


def find_path_links(properties: list, fuzz_data: FuzzData) -> list:
    links = []

    for prop in properties:
        property_hops: list = find_property_hops(prop, fuzz_data)
        property_links: list = parse_hops2links(property_hops, fuzz_data)
        links.append(property_links)

    return links


def find_property_hops(prop: dict, fuzz_data: FuzzData) -> list:
    """ Find the networks associated with each property

    :return: a set of IP addresses (without a netmask)
    """
    vm_ip: str = prop["vm_ip"]
    src_dev: str = prop["container_name"]
    dest_network: str = prop["dest_sim_net"]

    nets = []

    while True:
        next_hops_output: str = exec_next_hop_find(vm_ip, src_dev, dest_network)
        next_hops: list = next_hops_output.split(",")

        if len(next_hops) == 1:
            nets.append(next_hops[0])
            break
        elif not next_hops:
            print(clr("No path to {}".format(dest_network), 'red'))
            break
        else:
            src_dev = fuzz_data.find_ip_device(next_hops[1])
            vm_ip = fuzz_data.find_container_vm(src_dev)

            if not src_dev or not vm_ip:
                print(clr("Next hop {} on {} not present {}".
                          format(src_dev, vm_ip, dest_network), 'red'))
                break

            nets.extend(next_hops[1:])

    return nets


def exec_next_hop_find(vm_ip, src_dev, dest_network) -> str:
    """ Execute the next hop finding script and return a
    comma separated string of IP addresses without a netmask """
    result = subprocess.run([const.FIB_NEXT_HOP_SH, vm_ip, src_dev, dest_network],
                            stdout=subprocess.PIPE)
    next_hops: str = result.stdout.decode('utf-8')

    return next_hops


def parse_hops2links(property_hops: list, fuzz_data) -> list:
    links = []

    for hop in property_hops:
        hop_iface = "{}/24".format(hop)
        hop_network: str = str(ipaddress.IPv4Interface(hop_iface).network)
        links.append(fuzz_data.get_sim_net_name(hop_network))

    return links


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
