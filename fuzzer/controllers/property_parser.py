""" Reachability parser

Responsible for parsing the reachability properties specified as input.

Public functions:
    * parse_properties
"""

from fuzzer.common import file_reader as fr
from fuzzer.common import file_writer as fw
from fuzzer.common.FuzzData import FuzzData


def parse_properties(fuzz_data: FuzzData) -> dict:
    # TODO make this read all properties
    raw_reach_props: dict = fr.read_properties("reachability")
    reach_props: dict = parse_reachability_props(raw_reach_props, fuzz_data)

    fw.write_reach_instr(reach_props)
    fw.write_parsed_properties(reach_props)

    return reach_props


def parse_reachability_props(raw_properties, fuzz_data) -> dict:
    properties = dict()
    topo_name: str = fuzz_data.get_topo_name()

    for idx, raw_property in enumerate(raw_properties, start=1):
        prop = dict()
        container_name = get_container_name(topo_name, raw_property["src"])
        dest_sim_ip, dest_sim_net = fuzz_data.get_nat_ip(raw_property["dest"])

        prop["vm_ip"] = fuzz_data.find_container_vm(container_name)
        prop["container_name"] = container_name
        prop["dest_sim_ip"] = dest_sim_ip
        prop["dest_sim_net"] = dest_sim_net
        prop["dest_ip"] = raw_property["dest"]

        properties.update({idx: prop})

    return properties


def get_container_name(topo_name: str, container: str) -> str:
    return "{}-{}".format(topo_name, container)
