""" Reachability parser

Responsible for parsing the reachability properties specified as input.

Public functions:
    * parse_reachability
"""

from fuzzer.common import file_reader as fr
from fuzzer.common import file_writer as fw
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import fuzz_data_ops as fdata_ops


def parse_properties(fuzz_data: FuzzData):
    reach_properties: dict = fr.read_properties("reachability")
    topo_name: str = fuzz_data.get_topo_name()
    containers: dict = fuzz_data.get_containers()
    vms: dict = fuzz_data.get_vms()
    nat_ips: dict = fuzz_data.get_nat_ips()

    reachability_properties: list = __parse_reachability_props(reach_properties, topo_name,
                                                               containers, vms, nat_ips)
    fw.write_reach_instr(reachability_properties)
    fw.write_parsed_properties(reachability_properties)


def __parse_reachability_props(raw_properties, topo_name, containers, vms, nat_ips) -> list:
    properties = []

    for raw_property in raw_properties:
        prop = dict()
        prop["vm_ip"] = fdata_ops.find_container_vm(raw_property["src"],
                                                    containers, vms)
        prop["container_name"] = get_container_name(topo_name,
                                                    raw_property["src"])
        prop["dest_ip"] = raw_property["dest"]
        prop["dest_sim_ip"] = fdata_ops.get_nat_ip(raw_property["dest"], nat_ips)

        properties.append(prop)

    return properties


def get_container_name(topo_name: str, container: str) -> str:
    return "{}-{}".format(topo_name, container)
