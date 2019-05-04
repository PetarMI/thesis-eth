def parse_links(raw_links: dict) -> dict:
    """ Main function for parsing links between hosts """
    validate_links(raw_links)
    links: dict = assign_sim_nets(raw_links)

    return links


def assign_sim_nets(raw_links) -> dict:
    """ Create simulated networks and assign each link to one """
    links = dict()

    for host, host_links in raw_links.items():
        links.setdefault(host, {})
        for endpoint in host_links:
            sim_net = get_sim_net(host, endpoint, links)
            links[host].update({endpoint: sim_net})

    return links


def get_sim_net(host: str, endpoint: str, links: dict) -> str:
    if links.get(endpoint, None):
        sim_net: str = links[endpoint][host]
    else:
        sim_net: str = get_net_name(host, endpoint)

    return sim_net


def get_net_name(host: str, endpoint: str) -> str:
    return "net-{}-{}".format(host.lower(), endpoint.lower())


def validate_links(raw_links: dict):
    """ Ensure hosts have a duplex link in links file """
    for host, host_links in raw_links.items():
        for endpoint in host_links:
            if not raw_links.get(endpoint, None):
                raise ValueError("Missing top-level entry for host {}".format(endpoint))

            if host not in raw_links[endpoint]:
                raise ValueError("No duplex link between {} and {}".format(host, endpoint))
