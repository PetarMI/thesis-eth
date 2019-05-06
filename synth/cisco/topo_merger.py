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


# @Tested
def find_host_nets(host: str, host_ifaces: list, host_links: dict, host_neighbours: dict) -> list:
    """ Assign a net to each of the host's interfaces

    :param host: Hostname
    :param host_ifaces: List of the host's interfaces (each is a dict)
    :param host_links: The networks the host is connected to already
    :param host_neighbours: All of the host's neighbours
    :return: List of all the interfaces in dict format
    """
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


# @Tested
def search_neighbours(host_network, neighbours: dict, host_links: dict) -> str:
    """ Check what network a host's interface is connected to

    :param host_network: The network we are trying to match
    :param neighbours: All the neighbours we are searching through
    :param host_links: The networks this host is connected to
    :return: Name of the network this interface is connected to if it exists
    """
    for neighbour, neighbour_ifaces in neighbours.items():
        match = search_neighbour_ifaces(host_network, neighbour_ifaces)

        if match:
            sanity_check_link_exists(host_links.get(neighbour, None))
            return host_links[neighbour]

    return ""


# @Tested
def search_neighbour_ifaces(host_network, neighbour_ifaces: list) -> bool:
    """ Check if the neighbour has an interface belonging to the same network

    :param host_network: The host's iface we are matching belongs to this net
    :param neighbour_ifaces: all interfaces of a single neighbour
    :return: boolean indicating if the neghbour has an iface on the same net
    """
    match = False

    for neighbour_iface in neighbour_ifaces:
        neighbour_ip = ipaddress.IPv4Interface(neighbour_iface["ip"])

        if host_network == neighbour_ip.network:
            return True

    return match


def generate_simplex_net(host: str) -> str:
    return "net-{}".format(host.lower())


# @Tested
def get_neighbours_ifaces(host_neighbours, configs: dict) -> dict:
    """ Get only the neighbouring configurations (just interfaces)

    :param host_neighbours: list of neighbour names
    :param configs: all loaded configs
    :return: dictionary of neighbours and their interfaces
    """
    neighbours = dict()

    for neighbour in host_neighbours:
        neighbour_interfaces: list = configs[neighbour]["interfaces"]
        neighbours.update({neighbour: neighbour_interfaces})

    return neighbours


def sanity_check_link_exists(net: str):
    """ Just so I can sleep at night """
    if net is None:
        raise ValueError("Sanity check: Network match found in neighbours but "
                         "host has no link to that neighbour")

    if net == "":
        raise ValueError("Sanity check: Network match found in neighbours but "
                         "net name is empty")
