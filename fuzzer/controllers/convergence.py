from subprocess import call
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData


def converge_drop(dropped_nets: list):
    arg_nets: str = parse_network_params(dropped_nets)
    exec_convergence_monitor("-d", arg_nets)


def converge_full_revert(restored_nets: list):
    arg_nets: str = parse_network_params(restored_nets)
    exec_convergence_monitor("-f", arg_nets)


def converge_partial_revert(restored_nets: list, fuzz_data: FuzzData):
    arg_containers: str = parse_container_params(restored_nets, fuzz_data)
    exec_convergence_monitor("-p", arg_containers)


def exec_convergence_monitor(option: str, args: str):
    command = [const.CONVERGENCE_SH, option, args]

    return_code: int = call(command)
    signal_script_fail(return_code)


# TODO see what to do with empty lists
def parse_network_params(networks: list) -> str:
    parsed_nets = ','.join(networks)

    return parsed_nets


def parse_container_params(networks: list, fuzz_data: FuzzData) -> str:
    affected_containers = []

    for net_ip in networks:
        net_name: str = fuzz_data.get_sim_net_name(net_ip)
        net_devices: list = fuzz_data.find_network_devices(net_name)

        if len(net_devices) > 1:
            affected_containers.extend(net_devices)

    affected_containers = list(set(affected_containers))

    parsed_containers = ','.join(affected_containers)
    print(parsed_containers)
    return parsed_containers


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
