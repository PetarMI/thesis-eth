from fuzzer.controllers import Transition as t


###############################################################################
# ######################## PARTIAL REVERT #####################################
###############################################################################
def test_partial_no_dropped():
    dropped_links = []
    next_state = ('a',)

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": [],
        "drop": ['a']
    }

    assert(res_changes == expected_changes)


def test_partial_same():
    dropped_links = ['a']
    next_state = ('a',)

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": [],
        "drop": []
    }

    assert(res_changes == expected_changes)


def test_partial_more_dropped_overlap():
    dropped_links = ['a', 'c', 'v']
    next_state = ('a',)

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['c', 'v'],
        "drop": []
    }

    assert(res_changes == expected_changes)


def test_partial_more_dropped_no_overlap():
    dropped_links = ['a', 'c', 'v']
    next_state = ('d',)

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['a', 'c', 'v'],
        "drop": ['d']
    }

    assert(res_changes == expected_changes)


def test_partial_more_to_drop_overlap():
    dropped_links = ['a']
    next_state = ('a', 'b', 'c')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": [],
        "drop": ['b', 'c']
    }

    assert(res_changes == expected_changes)


def test_partial_more_to_drop_no_overlap():
    dropped_links = ['a']
    next_state = ('b', 'c', 'd')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['a'],
        "drop": ['b', 'c', 'd']
    }

    assert(res_changes == expected_changes)


def test_partial_random1():
    dropped_links = ['a', 'f']
    next_state = ('b', 'c', 'd')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['a', 'f'],
        "drop": ['b', 'c', 'd']
    }

    assert(res_changes == expected_changes)


def test_partial_random2():
    dropped_links = ['a', 'f', 'r', 'p', 'q']
    next_state = ('b', 'c', 'd')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['a', 'f', 'r', 'p', 'q'],
        "drop": ['b', 'c', 'd']
    }

    assert(res_changes == expected_changes)


def test_partial_random3():
    dropped_links = ['a', 'b', 'c', 'd', 'e', 'f']
    next_state = ('b', 'g', 'f')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['a', 'c', 'd', 'e'],
        "drop": ['g']
    }

    assert(res_changes == expected_changes)


def test_partial_random4():
    dropped_links = ['b', 'f', 'g']
    next_state = ('a', 'b', 'c', 'd', 'e', 'f')

    res_changes = t.PartialRevert.find_link_changes(dropped_links, next_state)
    expected_changes = {
        "restore": ['g'],
        "drop": ['a', 'c', 'd', 'e']
    }

    assert(res_changes == expected_changes)
