import subprocess
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import file_writer as fw


def verify_fib_reachability(properties: list, fuzz_data: FuzzData) -> dict:
    ver_results = dict()

    for idx, prop in enumerate(properties, start=1):
        print("Verifying {}".format(idx))
        reachability_res = verify_fib_property(prop, fuzz_data)
        ver_results.update({idx: reachability_res})

    return ver_results


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
            break
        elif not next_hop:
            print(next_hop)
            ver_status = 1
            ver_msg = "No path to network {} at device {}".format(dest_network, src_dev)
            break
        else:
            src_dev = fuzz_data.find_ip_device(next_hop)
            vm_ip = fuzz_data.find_container_vm(src_dev)

            if not src_dev or not vm_ip:
                ver_status = 2
                ver_msg = "Next hop {} on {} not present".format(src_dev, vm_ip)
                break

    return {
        "status": ver_status,
        "desc": ver_msg
    }


def exec_fib_verification(vm_ip, src_dev, dest_network) -> subprocess.CompletedProcess:
    """ Call the verifier script for one property """
    result = subprocess.run([const.FIB_SH, vm_ip, src_dev, dest_network],
                            stdout=subprocess.PIPE)

    return result


def interpret_verification_results(state: tuple, fib_results: dict):
    all_successful: bool = True
    failures = []

    for property_id, ver_res in fib_results.items():
        if ver_res["status"] == 0:
            continue
        else:
            all_successful = False

        pretty_print_failure(property_id, ver_res)

        failures.append({
            "pid": property_id,
            "desc": ver_res["desc"],
        })

    if all_successful:
        print(clr("All properties HOLD", 'green'))
    else:
        fw.write_state_failures(state, failures)


def pretty_print_failure(pid: int, verification_res: dict):
    ver_status = verification_res["status"]

    if ver_status == 1:
        print(clr("Property {} FAILED: {}".format(pid, verification_res["desc"]), 'red'))
    elif ver_status == 2:
        print(clr("Property {} ERROR: {}".format(pid, verification_res["desc"]), 'grey'))
