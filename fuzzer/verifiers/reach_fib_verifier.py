import time
import ipaddress
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common import file_writer as fw
from fuzzer.controllers.fib import Fib


def verify_fib_reachability(properties: dict, fib, fuzz_data, failed_nets: list) -> dict:
    failed_properties = dict()

    # remember the properties that failed
    for prop_id, prop in properties.items():
        # print("Verifying property {}".format(prop_id))
        reachability_res = verify_fib_property(prop, fib, fuzz_data, failed_nets)

        if reachability_res["status"] != 0:
            failed_properties.update({prop_id: prop})

    # double check to give network more time to converge
    if failed_properties:
        property_failures = double_check_violations(failed_properties, fib, fuzz_data, failed_nets)
        pretty_print_double_check_info(failed_properties, property_failures)
        return property_failures
    else:
        # just and empty dict signaling all properties hold
        return failed_properties


def double_check_violations(failed_properties: dict, fib: Fib, fuzz_data, failed_nets) -> dict:
    print(clr("## Giving network {} seconds to converge before double checking".
              format(const.CONV_TIME), 'cyan'))
    time.sleep(const.CONV_TIME)

    property_failures = dict()

    for prop_id, prop in failed_properties.items():
        print("Double checking property {}".format(prop_id))
        reachability_res = verify_fib_property(prop, fib, fuzz_data, failed_nets)

        if reachability_res["status"] != 0:
            property_failures.update({prop_id: reachability_res})

    return property_failures


def verify_fib_property(prop: dict, fib: Fib, fuzz_data, failed_nets):
    src_dev: str = prop["container_name"]
    dest_network: str = prop["dest_sim_net"]

    while True:
        next_hops: list = fib.find_next_hops(src_dev, dest_network)

        if next_hops == []:
            ver_status = 0
            ver_msg = "Found path to network {}".format(dest_network)
            ver_info = ""
            break
        elif next_hops is None:
            ver_status = 1
            ver_msg = "No reachability from {} to {}".format(src_dev, prop["dest_sim_ip"])
            ver_info = "No path to network {} at device {}".format(dest_network, src_dev)
            break
        else:
            if check_next_hop_failed(next_hops[0], failed_nets):
                ver_status = 1
                ver_msg = "No reachability from {} to {}".format(src_dev, prop["dest_sim_ip"])
                ver_info = "Next hop {} at {} is on a failed link".format(next_hops[0], src_dev)
                break

            src_dev = fuzz_data.find_ip_device(next_hops[0])

            if src_dev is None:
                ver_status = 2
                ver_msg = "No reachability from {} to {}".format(src_dev, prop["dest_sim_ip"])
                ver_info = "Next hop {} not present".format(src_dev)
                break

    return {
        "status": ver_status,
        "desc": ver_msg,
        "info": ver_info
    }


# @Tested
def check_next_hop_failed(next_hop: str, failed_nets: list) -> bool:
    """ Check if the next hop belongs to a failed network """
    next_hop_ip = ipaddress.IPv4Address(next_hop)

    for fnet in failed_nets:
        if next_hop_ip in ipaddress.IPv4Network(fnet, strict=True):
            return True

    return False


def examine_violations(state, reach_iterations, property_failures: dict):
    if property_failures:
        pretty_print_violations(property_failures)
        fw.track_reach_progress(reach_iterations, property_failures)
        fw.write_state_failures(state, property_failures)
    else:
        print(clr("All properties HOLD", 'green'))


def pretty_print_violations(property_failures: dict):
    for prop_id, ver_res in property_failures.items():
        ver_status = ver_res["status"]

        if ver_status == 1:
            print(clr("Property {} FAILED: {}".format(prop_id, ver_res["desc"]), 'red'))
        elif ver_status == 2:
            print(clr("Property {} ERROR: {}".format(prop_id, ver_res["desc"]), 'grey'))

        print(clr("\tInfo: {}".format(ver_res["info"]), 'yellow'))


def pretty_print_double_check_info(first_pass_fails: dict, double_check_fails):
    num_fp_fails: int = len(first_pass_fails.keys())
    num_dc_fails: int = len(double_check_fails.keys())

    if num_fp_fails == num_dc_fails:
        print("INFO: All {} failed properties still fail after double checking".
              format(num_fp_fails))
    elif num_dc_fails == 0:
        print("INFO: All failed properties succeeded after double checking")
    else:
        print("INFO: Some failed properties succeeded after double checking")
