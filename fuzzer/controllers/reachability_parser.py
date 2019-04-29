import ipaddress
import file_reader as fr
import file_writer as fw


def main():
    reach_properties: dict = fr.read_properties("reachability")
    vms: dict = fr.read_vm_info()
    topo: dict = fr.read_topo()
    nat_ips: dict = fr.read_nat_ips()

    properties: list = parse_properties(reach_properties, vms, topo, nat_ips)
    fw.write_reach_file(properties)


def parse_properties(raw_properties, vms, topo, nat_ips) -> list:
    properties = []

    for raw_property in raw_properties:
        prop = dict()
        prop["vm_ip"] = get_vm_ip(raw_property, topo["containers"], vms)
        prop["container_name"] = get_container_name(topo["meta"]["name"],
                                                    raw_property["src"])
        prop["dest_ip"] = get_nat_ip(raw_property["dest"], nat_ips)

        properties.append(prop)

    return properties


def get_vm_ip(prop: dict, topo_containers: dict, vms: dict) -> str:
    """ Find the VM IP on which the container is running """

    src_name = prop["src"]
    vm_id = None

    for container in topo_containers:
        if src_name == container["name"]:
            vm_id = container["vm"]

    if vm_id is None:
        raise ValueError("Property src container not in topo file {}".format(src_name))

    vm = vms.get(vm_id, None)

    if vm is None:
        raise ValueError("No running VM with ID {}".format(vm_id))

    return vm["ip"]


# TODO this is dealing with reachability addresses specified without netmask
# function wouldn't need to cast if the reachability address was given one
def get_nat_ip(dest_ip: str, nat_ips: dict) -> str:
    casted_dest_ip = ipaddress.IPv4Address(dest_ip)

    for cont_ips in nat_ips.values():
        for orig_iface in cont_ips.keys():
            casted_orig_ip = orig_iface.ip
            if casted_dest_ip == casted_orig_ip:
                return cont_ips[orig_iface]

    raise ValueError("Original IP {} not in NAT logs".format(dest_ip))


def get_container_name(topo_name: str, container: str) -> str:
    return "{}-{}".format(topo_name, container)


if __name__ == '__main__':
    main()
