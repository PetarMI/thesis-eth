import ipaddress
import file_reader as fr


def perform_match(topo_name: str) -> dict:
    orig_ifaces: dict = fr.read_orig_ifaces(topo_name)
    sim_ifaces: dict = fr.read_sim_ifaces(topo_name)
    matched_subnets: dict = fr.read_matched_subnets(topo_name)

    # this shouldn't really happen but check the return value anyway
    if (not make_sanity_checks(orig_ifaces, sim_ifaces)):
        exit(1)

    # matched_ips, matched_ifaces =
    match(orig_ifaces, sim_ifaces, matched_subnets)


def match(orig_ifaces: dict, sim_ifaces: dict, matched_subnets: dict):
    for dev, orig_config in orig_ifaces.items():
        sim_config: dict = sim_ifaces.get(dev)

        ifaces = {}
        ips = {}

        #for o_iface, o_ip in orig_config.items():
            #sim_subnet = find_sim_subnet(o_ip, matched_subnets)


#def find_sim_subnet(ip: str, matched_subnets: dict):
    #for o_subnet, sim_subnet in matched_subnets.items():
        #if


def make_sanity_checks(o_ifaces: dict, s_ifaces: dict) -> bool:
    return True


perform_match("toy")
