""" Reachability parser

Responsible for parsing the reachability properties specified as input.

Public functions:
    * parse_properties
"""

from fuzzer.common import file_reader as fr
from fuzzer.common import file_writer as fw
from fuzzer.common.FuzzData import FuzzData


def parse_properties(fuzz_data: FuzzData) -> dict:
    raw_props: dict = fr.read_properties()
    reach_props: dict = parse_reachability_props(raw_props["reachability"], fuzz_data)

    fw.write_reach_instr(reach_props)
    fw.write_reach_properties(reach_props)

    return reach_props


def parse_reachability_props(raw_reach_props, fuzz_data) -> dict:
    properties = dict()
    topo_name = fuzz_data.get_topo()["meta"]["name"]

    for idx, raw_property in enumerate(raw_reach_props, start=1):
        prop = dict()
        container_name = prepend_topo(topo_name, raw_property["src"])
        dest_sim_ip, dest_sim_net = fuzz_data.get_nat_ip(raw_property["dest"])

        prop["vm_ip"] = fuzz_data.find_container_vm(container_name)
        prop["container_name"] = container_name
        prop["dest_sim_ip"] = dest_sim_ip
        prop["dest_sim_net"] = dest_sim_net
        prop["dest_ip"] = raw_property["dest"]

        properties.update({idx: prop})

    return properties


def parse_iso_props(raw_iso_props: list, fuzz_data: FuzzData) -> dict:
    iso_properties = dict()
    topo: dict = fuzz_data.get_topo()
    ospf_links = fuzz_data.get_ospf_networks()

    for idx, raw_property in enumerate(raw_iso_props, start=1):
        iso_prop = dict()
        dest_sim_ip, dest_sim_net = fuzz_data.get_nat_ip(raw_property["dest"])

        iso_prop["src_name"] = prepend_topo(topo["meta"]["name"], raw_property["src"])
        iso_prop["dest_sim_net"] = dest_sim_net
        iso_prop["trap_ips"] = find_trap_ips(raw_property["traps"], topo,
                                             ospf_links, fuzz_data)

        iso_properties.update({idx: iso_prop})

    return iso_properties


def find_trap_ips(trap_nodes: list, topo: dict, ospf_links, fuzz_data: FuzzData) -> list:
    trap_ips = []
    topo_name = fuzz_data.get_topo()["meta"]["name"]

    for trap_node in trap_nodes:
        node_ifaces = find_container_ifaces(topo, trap_node)
        trap_ips.extend(find_ospf_ips(node_ifaces, ospf_links, topo_name, fuzz_data))

    return trap_ips


def find_container_ifaces(topo: dict, container_name) -> list:
    for cont in topo["containers"]:
        if cont["name"] == container_name:
            return cont["interfaces"]

    raise ValueError("Container {} not found in topo file".format(container_name))


def find_ospf_ips(node_ifaces: list, ospf_links, topo_name, fuzz_data: FuzzData) -> list:
    ospf_ips = []

    for iface in node_ifaces:
        sim_iface_name = prepend_topo(topo_name, iface["name"])

        if sim_iface_name in ospf_links:
            dest_sim_ip, dest_sim_net = fuzz_data.get_nat_ip(iface["ipaddr"])
            ospf_ips.append(dest_sim_ip)

    return ospf_ips


def prepend_topo(topo_name: str, entity: str) -> str:
    return "{}-{}".format(topo_name, entity)
