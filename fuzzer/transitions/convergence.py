from subprocess import call
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const


def converge_drop(dropped_nets: list):
    arg_nets: str = parse_convergence_params(dropped_nets)
    exec_convergence_monitor("-d", arg_nets)


def converge_full_revert(restored_nets: list):
    arg_nets: str = parse_convergence_params(restored_nets)
    exec_convergence_monitor("-f", arg_nets)


def converge_partial_revert(restored_containers: list):
    """ Call the convergence script with a list of containers which will have
        an increased number of neighbors after restoring some links """
    arg_containers: str = parse_convergence_params(restored_containers)
    exec_convergence_monitor("-p", arg_containers)


# TODO does it make sense to call with empty param list
def exec_convergence_monitor(option: str, args: str):
    command = [const.CONVERGENCE_SH, option, args]

    return_code: int = call(command)
    signal_script_fail(return_code)


# TODO see what to do with empty lists
def parse_convergence_params(entities: list) -> str:
    """ Parse the network IPs that need to be passed as a script argument """
    parsed_nets = ','.join(entities)

    return parsed_nets


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
