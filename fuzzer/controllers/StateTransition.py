""" State transition implementation

My attempt at imitating a polymorphic set of classes in Python.
`Transition` can be seen as the interface which declares function
`find_link_changes()`

Each class then has its own implementation of the "interface" method
"""
from subprocess import call
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const


class FullRevert:
    """ Restores ALL dropped links between every state transition"""
    # TODO tests
    @staticmethod
    def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
        return {
            "restore": dropped_links,
            "drop": list(next_state)
        }

    @staticmethod
    def exec_state_transition(transition_instr: dict, net_changes: dict):
        _exec_state_transition(transition_instr, net_changes, strict=True)


# TODO: not finished
class PartialRevert:
    """ Restore only non-overlapping links between state transitions"""
    # @Tested
    @staticmethod
    def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
        links_to_restore = state_diff(dropped_links, next_state)
        links_to_drop = state_diff(next_state, dropped_links)

        return {
            "restore": links_to_restore,
            "drop": links_to_drop
        }

    @staticmethod
    def exec_state_transition(transition_instr: dict, net_changes: dict):
        _exec_state_transition(transition_instr, net_changes, strict=False)


###############################################################################
# ############### Common functions between the two classes ####################
###############################################################################
def _exec_state_transition(transition_instr: dict, net_changes: dict, strict: bool):
    print(clr("## Restoring dropped links", 'cyan'))
    exec_link_changes(transition_instr.get(const.RESTORE))
    exec_convergence_wait(const.RESTORE, net_changes, strict)

    print(clr("## Dropping failed links", 'cyan'))
    exec_link_changes(transition_instr.get(const.DROP))
    exec_convergence_wait(const.DROP, net_changes)


def exec_link_changes(instructions: list):
    """ Call an executor script to execute each change """
    for n, instr in enumerate(instructions, start=1):
        pretty_print_instr(instr, n, len(instructions))
        return_code: int = call([const.LINK_STATE_SH, "-f", "iface",
                                 "-v", instr["vm"], "-d", instr["container"],
                                 "-i", instr["iface"], "-s", instr["op_type"]])
        signal_script_fail(return_code, "{} interface {}".
                           format(instr["op_type"], instr["iface"]))


def exec_convergence_wait(op: str, net_changes: dict, strict=True):
    command = [const.CONVERGENCE_SH]
    command.extend(parse_convergence_params(op, net_changes.get(op), strict))

    return_code: int = call(command)
    signal_script_fail(return_code)


# TODO see what to do with empty lists
def parse_convergence_params(op: str, networks: list, strict: bool) -> list:
    params = []

    if op == const.DROP:
        params.append("-d")
    elif op == const.RESTORE:
        params.append("-r")

    params.append(','.join(networks))

    if strict:
        params.append("-s")

    return params


def pretty_print_instr(instr: dict, n, t):
    progress = "({}/{})".format(n, t)
    op = "Dropping" if instr["op_type"] == "drop" else "Restoring"

    print("{} {} link {} on device {}".
          format(progress, op, instr["link"], instr["container"]))


# @Tested (as part of calling function find_link_changes)
def state_diff(state_a, state_b) -> list:
    """ Difference between two lists/tuples (elements that are in A but not B)
    Preferred to setA.difference(setB) since the later is non-deterministic
    Later may be asymptotically faster but here we will only diff lists of 2-3 elements
    """
    diff = []

    for state in state_a:
        if state not in state_b:
            diff.append(state)

    return diff


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
