import ipaddress
from synth.common import file_writer as fw


def generate_topo(topo_data: dict, topo_name: str) -> dict:
    networks: list = extract_networks(topo_data)
    containers: list = generate_containers(topo_data)
    meta: dict = generate_meta(topo_name)

    topo = dict()
    topo.update({"meta": meta})
    topo.update({"networks": networks})
    topo.update({"containers": containers})

    fw.write_topo_file(topo_name, topo)
    return topo


def extract_networks(topo_data: dict) -> list:
    topo_networks = []
    networks_track = dict()

    for host, host_interfaces in topo_data.items():
        for interface in host_interfaces:
            if not check_network_exists(interface, networks_track):
                unseen_net: dict = construct_net(interface)
                topo_networks.append(unseen_net)
                networks_track.update({
                    unseen_net["name"]: unseen_net["subnet"]
                })

    return topo_networks


def generate_containers(topo_data: dict) -> list:
    topo_containers: list = []

    for host, host_interfaces in topo_data.items():
        container: dict = construct_container(host)
        container_interfaces: list = extract_container_networks(host_interfaces)

        container.update({"interfaces": container_interfaces})
        topo_containers.append(container)

    return topo_containers


def check_network_exists(interface: dict, networks_track) -> bool:
    interface_network = interface["net"]

    if interface_network in networks_track:
        validate_duplicate_subnet(interface["subnet"],
                                  networks_track[interface_network])
        return True

    return False


def validate_duplicate_subnet(duplicate_subnet: str, saved_subnet: str):
    """ Ensure that if network with same name is found it has the same subnet

    :param duplicate_subnet: Network with matching name
    :param saved_subnet: Network which exists in the tracking list
    """
    parsed_duplicate = ipaddress.IPv4Network(duplicate_subnet, strict=True)
    parsed_saved = ipaddress.IPv4Network(saved_subnet, strict=True)

    if not parsed_duplicate == parsed_saved:
        raise ValueError("Networks with same name but different subnets {} and {}"
                         .format(duplicate_subnet, saved_subnet))


def construct_net(interface: dict) -> dict:
    net = {
        "name": interface["net"],
        "subnet": interface["subnet"]
    }

    return net


def extract_container_networks(host_interfaces: list) -> list:
    parsed_interfaces: list = []

    for interface in host_interfaces:
        parsed_interfaces.append({
            "network": interface["net"],
            "ipaddr": interface["ip"]
        })

    return parsed_interfaces


def construct_container(host: str) -> dict:
    container = dict()

    container["name"] = host.lower()
    container["type"] = "frr"
    container["vm"] = "UNDEFINED"

    return container


def generate_meta(topo_name: str) -> dict:
    return {"name": topo_name}
