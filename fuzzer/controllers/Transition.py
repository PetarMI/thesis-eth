""" State transition implementation

My attempt at imitating a polymorphic set of classes in Python.
`Transition` can be seen as the interface which declares function
`find_link_changes()`

Each cass then has its own implementation of the "interface" method
"""


class FullRevert:
    """ Restores ALL dropped links between every state transition"""
    # TODO tests
    @staticmethod
    def find_link_changes(dropped_links: list, next_state: tuple) -> dict:
        return {
            "restore": dropped_links,
            "drop": list(next_state)
        }


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
