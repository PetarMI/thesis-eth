import file_reader as fr


def perform_match(topo_name: str) -> dict:
    """ Main function of subnet matching module """

    topo_nets: list = fr.read_topo_nets(topo_name)
    orig_subnets: dict = parse_orig_subnets(topo_name, topo_nets)
    sim_subnets = fr.read_sim_subnets(topo_name)

    # this shouldn't really happen but check the return value anyway
    if (not subnet_sanity_checks(orig_subnets, sim_subnets)):
        exit(1)

    subnets = match_subnets(orig_subnets, sim_subnets)

    return subnets


# @Tested
def parse_orig_subnets(topo_name: str, topo_nets: list) -> dict:
    subnets = {}

    for net in topo_nets:
        sim_name = update_net_name(topo_name, net["name"])
        if (sim_name in subnets.keys()):
            raise KeyError("Duplicate subnet")

        subnets.update({
            sim_name: net["subnet"]
        })

    return subnets


# @Tested
def match_subnets(orig_subnets: dict, sim_subnets: dict) -> dict:
    subnets = {}

    for net_name, o_subnet in orig_subnets.items():
        s_subnet = sim_subnets[net_name]

        subnets.update({
            o_subnet: s_subnet
        })

    return subnets


# @Tested
def update_net_name(topo_name, orig_net_name: str) -> str:
    return "{}-{}".format(topo_name, orig_net_name)


# @Tested
def subnet_sanity_checks(orig_subnets: dict, sim_subnets: dict) -> bool:
    if (len(orig_subnets) != len(sim_subnets)):
        raise KeyError("Network number mismatch")

    for o_net in orig_subnets.keys():
        if (o_net not in sim_subnets.keys()):
            raise KeyError("Network mismatch")

    return True
