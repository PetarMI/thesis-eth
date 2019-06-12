import subprocess
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData


def verify_fib_reachability(properties: list, fuzz_data: FuzzData) -> dict:
    ver_results = dict()

    for idx, prop in enumerate(properties):
        reachability_res = verify_fib_property(prop, fuzz_data)
        ver_results.update({idx: reachability_res})

    return ver_results


def verify_fib_property(prop: dict, fuzz_data: FuzzData):
    ver_result = dict()

    vm_ip: str = prop["vm_ip"]
    src_dev: str = prop["container_name"]
    dest_network: str = prop["dest_sim_net"]

    while True:
        reachability_res = exec_fib_verification(vm_ip, src_dev, dest_network)
        next_hop: str = reachability_res.stdout.decode('utf-8')

        if next_hop == "connected":
            ver_result["status"] = 0
            break
        elif not next_hop:
            ver_result["status"] = 1
            ver_result["endpoint"] = src_dev
            break
        else:
            src_dev = fuzz_data.find_ip_device(next_hop)
            vm_ip = fuzz_data.find_container_vm(src_dev)

            if not src_dev or not vm_ip:
                ver_result["status"] = 2
                ver_result["message"] = "Next hop {} on {} not present".format(
                    src_dev, vm_ip
                )
                break

    return ver_result


def exec_fib_verification(vm_ip, src_dev, dest_network) -> subprocess.CompletedProcess:
    """ Call the verifier script for one property """
    result = subprocess.run([const.FIB_SH, vm_ip, src_dev, dest_network],
                            stdout=subprocess.PIPE)

    return result
