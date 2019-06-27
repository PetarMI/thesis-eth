import subprocess
import time
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import file_writer as fw


def verify_fib_reachability(properties: dict, fuzz_data: FuzzData) -> dict:
    failed_properties = dict()

    # remember the properties that failed
    for prop_id, prop in properties.items():
        print("Verifying property {}".format(prop_id))
        reachability_res = verify_fib_property(prop, fuzz_data)

        if reachability_res["status"] != 0:
            failed_properties.update({prop_id: prop})

    # double check to give network more time to converge
    if failed_properties:
        return double_check_failed(failed_properties, fuzz_data)
    else:
        return failed_properties


def double_check_failed(failed_properties: dict, fuzz_data: FuzzData) -> dict:
    print(clr("# Giving network {} seconds to converge before double checking".
              format(const.CONV_TIME), 'cyan'))
    time.sleep(const.CONV_TIME)

    property_failures = dict()

    for prop_id, prop in failed_properties.items():
        print("Double checking property {}".format(prop_id))
        reachability_res = verify_fib_property(prop, fuzz_data)
        property_failures.update({prop_id: reachability_res})

    return property_failures


def verify_fib_property(prop: dict, fuzz_data: FuzzData):
    vm_ip: str = prop["vm_ip"]
    src_dev: str = prop["container_name"]
    dest_network: str = prop["dest_sim_net"]

    while True:
        reachability_res = exec_fib_verification(vm_ip, src_dev, dest_network)
        next_hop: str = reachability_res.stdout.decode('utf-8')

        if next_hop == "connected":
            ver_status = 0
            ver_msg = "Found path to network {}".format(dest_network)
            ver_info = ""
            break
        elif not next_hop:
            ver_status = 1
            ver_msg = "No reachability from {} to {}".format(src_dev, prop["dest_sim_ip"])
            ver_info = "No path to network {} at device {}".format(dest_network, src_dev)
            break
        else:
            src_dev = fuzz_data.find_ip_device(next_hop)
            vm_ip = fuzz_data.find_container_vm(src_dev)

            if not src_dev or not vm_ip:
                ver_status = 2
                ver_msg = "No reachability from {} to {}".format(src_dev, prop["dest_sim_ip"])
                ver_info = "Next hop {} on {} not present".format(src_dev, vm_ip)
                break

    return {
        "status": ver_status,
        "desc": ver_msg,
        "info": ver_info
    }


def exec_fib_verification(vm_ip, src_dev, dest_network) -> subprocess.CompletedProcess:
    """ Call the verifier script for one property """
    result = subprocess.run([const.FIB_SH, vm_ip, src_dev, dest_network],
                            stdout=subprocess.PIPE)

    return result


def examine_violations(state, property_failures: dict):
    if property_failures:
        pretty_print_violations(property_failures)
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
