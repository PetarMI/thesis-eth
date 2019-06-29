""" State transition implementation

My attempt at imitating a polymorphic set of classes in Python.
`Transition` can be seen as the interface which declares function
`find_link_changes()`

Each class then has its own implementation of the "interface" method
"""
from subprocess import call
from termcolor import colored as clr
from fuzzer.common import constants_fuzzer as const
from fuzzer.common.FuzzData import FuzzData
from fuzzer.transitions import convergence
from fuzzer.transitions.InstructionGenerator import InstructionGenerator


class PartialRevert:
    """ Restore only non-overlapping links between state transitions"""
    def __init__(self, fuzz_data: FuzzData):
        self.igen = InstructionGenerator(fuzz_data)
        self.dropped_links = []

    def perform_state_transition(self, state):
        link_changes: dict = self.find_link_changes(self.dropped_links, state)
        transition_instr: dict = self.igen.gen_transition_instructions(link_changes)
        transition_data: dict = self.igen.get_transition_data(link_changes)

        self.exec_state_transition(transition_instr, transition_data)
        self.dropped_links = state

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
    def exec_state_transition(transition_instr: dict, transition_data: dict):
        print(clr("## Dropping failed links", 'cyan'))
        exec_link_changes(transition_instr.get(const.DROP))
        convergence.converge_drop(transition_data[const.DROP])
        # save the state so that we check the number of neighbors after the restore is increased
        exec_state_save()

        print(clr("## Restoring non-overlapping links", 'cyan'))
        exec_link_changes(transition_instr[const.RESTORE])
        convergence.converge_partial_revert(transition_data[const.RESTORE])


###############################################################################
# ############### Common functions between the two classes ####################
###############################################################################
def exec_link_changes(instructions: list):
    """ Call an executor script to execute each change """
    for n, instr in enumerate(instructions, start=1):
        pretty_print_instr(instr, n, len(instructions))
        return_code: int = call([const.LINK_STATE_SH, "-f", "iface",
                                 "-v", instr["vm"], "-d", instr["container"],
                                 "-i", instr["iface"], "-s", instr["op_type"]])
        signal_script_fail(return_code, "{} interface {}".
                           format(instr["op_type"], instr["iface"]))


def exec_state_save():
    return_code: int = call([const.VM_STATE_SH, "-r"])
    signal_script_fail(return_code, "Saving running state")


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


class FullRevert:
    """ Reverts the topology to its initial state between state transitions """
    def __init__(self):
        self.exec_prepare_vms()

    def perform_state_transition(self, state):
        raise RuntimeError("Not implemented")

    # TODO tests
    @staticmethod
    def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
        return {
            "restore": dropped_links,
            "drop": list(next_state)
        }

    @staticmethod
    def exec_state_transition(transition_instr: dict, net_changes: dict):
        print(clr("## Reverting to initial state", 'cyan'))
        exec_link_changes(transition_instr[const.RESTORE])
        convergence.converge_full_revert(net_changes[const.RESTORE])

        print(clr("## Dropping failed links", 'cyan'))
        exec_link_changes(transition_instr.get(const.DROP))
        convergence.converge_drop(net_changes[const.DROP])

    @staticmethod
    def exec_prepare_vms():
        return_code: int = call([const.VM_STATE_SH, "-d"])
        signal_script_fail(return_code, "Preparing VMs for fuzzing")
