from fuzzer.controllers import StateTransition as t


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


###############################################################################
# ################################ OTHER ######################################
###############################################################################
def test_conv_param_parse_dropped():
    op = "drop"
    networks = ["10.0.1.0/24", "10.0.2.0/24"]

    res_params = t.parse_convergence_params(op, networks, False)
    expected_params = ["-d", "10.0.1.0/24,10.0.2.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_restored():
    op = "restore"
    networks = ["10.0.1.0/24", "10.0.4.0/24"]

    res_params = t.parse_convergence_params(op, networks, False)
    expected_params = ["-r", "10.0.1.0/24,10.0.4.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_strict():
    op = "restore"
    networks = ["10.0.1.0/24", "10.0.4.0/24"]

    res_params = t.parse_convergence_params(op, networks, True)
    expected_params = ["-r", "10.0.1.0/24,10.0.4.0/24", "-s"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_restored():
    link_changes = {
        "drop": ["10.0.1.0/24", "10.0.2.0/24"],
        "restore": []
    }

    res_params = t.parse_convergence_params(link_changes)
    expected_params = ["-d", "10.0.1.0/24,10.0.2.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_dropped():
    link_changes = {
        "restore": ["10.0.1.0/24", "10.0.2.0/24"],
        "drop": []
    }

    res_params = t.parse_convergence_params(link_changes)
    expected_params = ["-r", "10.0.1.0/24,10.0.2.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_changes():
    link_changes = {
        "restore": [],
        "drop": []
    }

    res_params = t.parse_convergence_params(link_changes)
    expected_params = []

    assert(res_params == expected_params)

