import ipaddress
from fuzzer.common import file_reader as fr
from fuzzer.common import file_writer as fw
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import fuzz_data_ops as fdata_ops


def main(fuzz_data: FuzzData):
    reach_properties: dict = fr.read_properties("reachability")
    nat_ips: dict = fr.read_nat_ips()

    properties: list = parse_properties(reach_properties, fuzz_data.topo_name,
                                        fuzz_data.containers, fuzz_data.vms,
                                        nat_ips)
    fw.write_reach_instr(properties)
    fw.write_parsed_properties(properties)


def parse_properties(raw_properties, topo_name, containers, vms, nat_ips) -> list:
    properties = []

    for raw_property in raw_properties:
        prop = dict()
        prop["vm_ip"] = fdata_ops.find_container_vm(raw_property["src"],
                                                    containers, vms)
        prop["container_name"] = get_container_name(topo_name,
                                                    raw_property["src"])
        prop["dest_ip"] = raw_property["dest"]
        prop["dest_sim_ip"] = get_nat_ip(raw_property["dest"], nat_ips)

        properties.append(prop)

    return properties


# TODO this is dealing with reachability addresses specified without netmask
# TODO improve this to not go over all the containers
def get_nat_ip(dest_ip: str, nat_ips: dict) -> str:
    casted_dest_ip = ipaddress.IPv4Address(dest_ip)

    for container in nat_ips.values():
        for orig_iface in container.keys():
            casted_orig_ip = orig_iface.ip

            if casted_dest_ip == casted_orig_ip:
                sim_dest_ip = container[orig_iface]
                return str(sim_dest_ip.ip)

    # raise ValueError("Original IP {} not in NAT logs".format(dest_ip))
    print("WARNING: Original IP {} not in NAT logs".format(dest_ip))
    return dest_ip


def get_container_name(topo_name: str, container: str) -> str:
    return "{}-{}".format(topo_name, container)
