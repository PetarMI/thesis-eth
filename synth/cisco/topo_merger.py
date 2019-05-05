import ipaddress


def merge_topo_data(links: dict, configs: dict) -> dict:
    topo = dict()

    for host, host_configs in configs.items():
        host_ifaces: list = host_configs["interfaces"]
        host_links: dict = links[host]
        host_neighbours: dict = get_neighbours_ifaces(host_links.keys(), configs)

        host_nets = find_host_nets(host, host_ifaces, host_links, host_neighbours)
        topo.update({host: host_nets})

    return topo


def find_host_nets(host: str, host_ifaces: list, host_links: dict, host_neighbours: dict) -> list:
    nets = []

    for host_iface in host_ifaces:
        host_network = ipaddress.IPv4Interface(host_iface["ip"]).network
        iface_net = search_neighbours(host_network, host_neighbours, host_links)

        if not iface_net:
            iface_net = generate_simplex_net(host)

        nets.append({
            "ip": host_iface["ip"],
            "net": iface_net,
            "subnet": str(host_network)
        })

    return nets


def search_neighbours(host_network, neighbours: dict, host_links: dict) -> str:
    for neighbour, neighbour_ifaces in neighbours.items():
        match = search_neighbour_ifaces(host_network, neighbour_ifaces)

        if match:
            return host_links[neighbour]

    return ""


def search_neighbour_ifaces(host_network, neighbour_ifaces: list) -> bool:
    match = False

    for neighbour_iface in neighbour_ifaces:
        neighbour_ip = ipaddress.IPv4Interface(neighbour_iface["ip"])

        if host_network == neighbour_ip.network:
            return True

    return match


def generate_simplex_net(host: str) -> str:
    return "net-{}".format(host.lower())


def get_neighbours_ifaces(host_neighbours, configs: dict) -> dict:
    neighbours = dict()

    for neighbour in host_neighbours:
        neighbour_interfaces: list = configs[neighbour]["interfaces"]
        neighbours.update({neighbour: neighbour_interfaces})

    return neighbours
