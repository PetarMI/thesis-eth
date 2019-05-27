""" Reachability parser

Responsible for parsing the reachability properties specified as input.

Public functions:
    * parse_properties
"""

from fuzzer.common import file_reader as fr
from fuzzer.common import file_writer as fw
from fuzzer.common.FuzzData import FuzzData


def parse_properties(fuzz_data: FuzzData):
    raw_reach_props: dict = fr.read_properties("reachability")
    reach_props: list = parse_reachability_props(raw_reach_props, fuzz_data)

    fw.write_reach_instr(reach_props)
    fw.write_parsed_properties(reach_props)


def parse_reachability_props(raw_properties, fuzz_data) -> list:
    properties = []
    topo_name: str = fuzz_data.get_topo_name()

    for raw_property in raw_properties:
        prop = dict()
        container_name = get_container_name(topo_name, raw_property["src"])

        prop["vm_ip"] = fuzz_data.find_container_vm(container_name)
        prop["container_name"] = container_name
        prop["dest_sim_ip"] = fuzz_data.get_nat_ip(raw_property["dest"])
        prop["dest_ip"] = raw_property["dest"]

        properties.append(prop)

    return properties


def get_container_name(topo_name: str, container: str) -> str:
    return "{}-{}".format(topo_name, container)
