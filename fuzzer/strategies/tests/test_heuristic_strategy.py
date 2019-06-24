import pytest
import heuristic_strategy as hs


###############################################################################
# ############################ HEURISTIC ######################################
###############################################################################
def test_complete_heuristic():
    property_links = ['b', 'd']
    all_links = ['a', 'b', 'c', 'd']

    res_plan = hs.heuristic(3, all_links, property_links)
    expected_plan = [
        (), ('b',), ('b', 'd'), ('d',),
        ('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'b', 'd'),
        ('a', 'c'), ('a', 'c', 'd'), ('a', 'd'),
        ('b', 'c'), ('b', 'c', 'd'), ('c',), ('c', 'd')
    ]

    assert(res_plan == expected_plan)


def test_complete_heuristic_longer():
    property_links = ['a', 'b', 'd']
    all_links = ['a', 'b', 'c', 'd']

    res_plan = hs.heuristic(3, all_links, property_links)
    expected_plan = [
        (), ('a',), ('a', 'b'), ('a', 'b', 'd'),
        ('a', 'd'), ('b',), ('b', 'd'), ('d',),
        ('a', 'b', 'c'), ('a', 'c'), ('a', 'c', 'd'),
        ('b', 'c'), ('b', 'c', 'd'), ('c',), ('c', 'd')
    ]

    assert(res_plan == expected_plan)


def test_complete_heuristic_even_longer():
    property_links = ['a', 'c', 'd']
    all_links = ['a', 'b', 'c', 'd']

    res_plan = hs.heuristic(4, all_links, property_links)
    expected_plan = [
        (), ('a',), ('a', 'c'), ('a', 'c', 'd'), ('a', 'd'), ('c',),
        ('c', 'd'), ('d',), ('a', 'b'), ('a', 'b', 'c'),
        ('a', 'b', 'c', 'd'), ('a', 'b', 'd'), ('b',), ('b', 'c'),
        ('b', 'c', 'd'), ('b', 'd'),

    ]

    assert(res_plan == expected_plan)


def test_gen_full_heuristic():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                 ('b', 'c'), ('c',)]

    res_plan = hs.gen_full_heuristic(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('b',),
                     ('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    assert(res_plan == expected_plan)


def test_gen_full_heuristic_no_overlap():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    res_plan = hs.gen_full_heuristic(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('b',),
                     ('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    assert(res_plan == expected_plan)


def test_gen_full_heuristic_full_overlap():
    subplan = [('a', 'c'), ('a',), ('a', 'b', 'c'), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',)]

    res_plan = hs.gen_full_heuristic(subplan, full_plan)
    expected_plan = [('a', 'c'), ('a',), ('a', 'b', 'c'), ('a', 'b'), ('b',)]

    assert(res_plan == expected_plan)


###############################################################################
# ###################### HEURISTIC VALIDATION #################################
###############################################################################
def test_heuristic_pre_validation():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                 ('b', 'c'), ('c',)]

    hs.pre_validate_heuristic_gen(subplan, full_plan)


def test_heuristic_pre_validation_not_subset():
    with pytest.raises(ValueError, match="Heuristic plan is not subset of the full plan"):
        subplan = [('a',), ('a', 'b'), ('b',), ('x',)]
        full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                     ('b', 'c'), ('c',)]

        hs.pre_validate_heuristic_gen(subplan, full_plan)


def test_heuristic_pre_validation_empty_plan():
    with pytest.raises(ValueError, match="Empty heuristic plan"):
        subplan = []
        full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                     ('b', 'c'), ('c',)]

        hs.pre_validate_heuristic_gen(subplan, full_plan)


def test_heuristic_pos_validation_ok():
    heuristic_plan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c')]

    hs.post_validate_heuristic_gen(heuristic_plan, full_plan)


def test_heuristic_pos_validation_not_ok():
    with pytest.raises(ValueError, match="Heuristic plan expected length - 2 vs real 3"):
        heuristic_plan = [('a',), ('a', 'b')]
        full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c')]

        hs.post_validate_heuristic_gen(heuristic_plan, full_plan)
