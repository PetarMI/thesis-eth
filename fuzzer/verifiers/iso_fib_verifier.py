import ipaddress
from termcolor import colored as clr
from fuzzer.controllers.fib import Fib
from fuzzer.common import file_writer as fw


def verify_fib_isolation(iso_props: dict, fib, fuzz_data, failed_nets: list) -> dict:
    failed_properties = dict()
    no_reach_props = dict()

    for prop_id, prop in iso_props.items():
        # print("Verifying property {}".format(prop_id))
        iso_res = verify_fib_property(prop, fib, fuzz_data, failed_nets)

        if iso_res["status"] == 1:
            failed_properties.update({prop_id: iso_res})
        elif iso_res["status"] == 2:
            no_reach_props.update({prop_id: iso_res})

    pretty_print_violations(no_reach_props)

    return failed_properties


def verify_fib_property(prop: dict, fib: Fib, fuzz_data, failed_nets):
    src_dev: str = prop["src_name"]
    dest_network: str = prop["dest_sim_net"]

    while True:
        next_hops: list = fib.find_next_hops(src_dev, dest_network)

        if next_hops == []:
            ver_status = 0
            ver_msg = "Path does not pass forbidden nodes"
            break
        elif next_hops is None:
            ver_status = 2
            ver_msg = "Broken reachability from {} to {}".format(src_dev, dest_network)
            break
        else:
            if check_next_hop_failed(next_hops[0], failed_nets):
                ver_status = 2
                ver_msg = "Broken reachability from {} to {}".format(src_dev, dest_network)
                break

            forbidden_hop: str = check_next_hops_forbidden(next_hops, prop["trap_ips"])

            if forbidden_hop:
                ver_status = 1
                ver_msg = "Path passes hop {}".format(forbidden_hop)
                break

            src_dev = fuzz_data.find_ip_device(next_hops[0])

            if src_dev is None:
                raise ValueError("Next hop {} not found in fuzz data".format(src_dev))

    return {
        "status": ver_status,
        "desc": ver_msg
    }


# @Tested
def check_next_hop_failed(next_hop: str, failed_nets: list) -> bool:
    """ Check if the next hop belongs to a failed network """
    next_hop_ip = ipaddress.IPv4Address(next_hop)

    for fnet in failed_nets:
        if next_hop_ip in ipaddress.IPv4Network(fnet, strict=True):
            return True

    return False


def check_next_hops_forbidden(next_hops: list, trap_ips: list):
    for next_hop in next_hops:
        if next_hop in trap_ips:
            return next_hop

    return False


def examine_violations(state, iso_iterations: int, property_failures: dict):
    if property_failures:
        pretty_print_violations(property_failures)
        fw.track_iso_progress(iso_iterations, property_failures)
        fw.write_state_failures(state, property_failures)
    else:
        print(clr("All properties HOLD", 'green'))


def pretty_print_violations(property_failures: dict):
    for prop_id, ver_res in property_failures.items():
        ver_status = ver_res["status"]

        if ver_status == 1:
            print(clr("Property {} FAILED: {}".format(prop_id, ver_res["desc"]), 'red'))
        elif ver_status == 2:
            print(clr("Property {}: {}".format(prop_id, ver_res["desc"]), 'yellow'))
