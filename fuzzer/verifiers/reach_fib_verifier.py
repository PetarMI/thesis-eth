from subprocess import call
from fuzzer.common import constants_fuzzer as const


def verify_ping_reachability(properties: list) -> dict:
    ver_results = dict()

    for idx, prop in enumerate(properties):
        vm_ip: str = prop["vm_ip"]
        src_dev: str = prop["container_name"]
        dest_network: str = prop["dest_sim_net"]

        reachability_res = exec_fib_verification(vm_ip, src_dev, dest_network)
        ver_results.update({idx: reachability_res})

    return ver_results


def exec_fib_verification(vm_ip, src_dev, dest_network) -> int:
    """ Call the verifier script for one property """
    return_code: int = call([const.FIB_SH,
                             "-m", vm_ip, "-s", src_dev, "-d", dest_network])

    return return_code
