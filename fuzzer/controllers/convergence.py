from subprocess import call
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const


def converge_full_revert(restored_nets: list):
    exec_convergence_monitor("-f", restored_nets)


def converge_partial_revert(restored_nets: list):
    exec_convergence_monitor("-p", restored_nets)


def converge_drop(dropped_nets: list):
    exec_convergence_monitor("-d", dropped_nets)


def exec_convergence_monitor(option: str, changed_nets: list):
    command = [const.CONVERGENCE_SH, option]
    command.append(parse_convergence_params(changed_nets))

    return_code: int = call(command)
    signal_script_fail(return_code)


# TODO see what to do with empty lists
def parse_convergence_params(networks: list) -> str:
    parsed_nets = ','.join(networks)

    return parsed_nets


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
