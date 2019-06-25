import pytest
import heuristic_strategy as hs


###############################################################################
# ######################### HEURISTIC FULL PLAN ###############################
###############################################################################
def test_heuristic_plan():
    heuristic_subplan = [(), ('a',), ('a', 'b'), ('a', 'c')]
    links = ['b', 'd', 'a', 'c']

    res_plan = hs.gen_full_plan(3, heuristic_subplan, links)
    expected_plan = [(), ('a',), ('a', 'b'), ('a', 'c'),
                     ('a', 'b', 'c'), ('a', 'b', 'd'), ('a', 'c', 'd'),
                     ('a', 'd'), ('b',), ('b', 'c'), ('b', 'c', 'd'),
                     ('b', 'd'), ('c',), ('c', 'd'), ('d',)
                     ]

    assert (res_plan == expected_plan)


###############################################################################
# ########################## HEURISTIC SUBPLAN ################################
###############################################################################
def test_heuristic_subplan():
    heuristic_links = [
        ['c', 'e', 'b'],
        ['a', 'b'],
        ['a', 'f', 'g', 'd'],
        ['d', 'f']
    ]

    res_plan = hs.gen_heuristic_subplan(3, heuristic_links)
    expected_plan = [
        (),
        ('b',), ('b', 'c'), ('b', 'c', 'e'), ('b', 'e'), ('c',), ('c', 'e'),
        ('e',),
        ('a',), ('a', 'b'),
        ('a', 'd'), ('a', 'd', 'f'), ('a', 'd', 'g'), ('a', 'f'), ('a', 'f', 'g'),
        ('a', 'g'), ('d',), ('d', 'f'), ('d', 'f', 'g'), ('d', 'g'), ('f',),
        ('f', 'g'), ('g',)
    ]

    assert (res_plan == expected_plan)


###############################################################################
# ########################### PLAN UNION ######################################
###############################################################################
def test_union_plans_full_overlap():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                 ('b', 'c'), ('c',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('b',),
                     ('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    assert (res_plan == expected_plan)


def test_union_plans_no_overlap():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('b',),
                     ('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    assert (res_plan == expected_plan)


def test_union_plans_identical():
    subplan = [('a', 'c'), ('a',), ('a', 'b', 'c'), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a', 'c'), ('a',), ('a', 'b', 'c'), ('a', 'b'), ('b',)]

    assert (res_plan == expected_plan)


def test_union_plans_some_overlap():
    subplan = [('a',), ('a', 'b'), ('b',)]
    full_plan = [('a',), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                 ('b', 'c'), ('c',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('b',),
                     ('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]

    assert (res_plan == expected_plan)


def test_union_plans_inverted_full_overlap():
    subplan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
               ('b', 'c'), ('c',)]
    full_plan = [('a',), ('a', 'b'), ('b',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                     ('b', 'c'), ('c',)]

    assert (res_plan == expected_plan)


def test_union_plans_inverted_no_overlap():
    subplan = [('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',)]
    full_plan = [('a',), ('a', 'b'), ('b',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a', 'b', 'c'), ('a', 'c'), ('b', 'c'), ('c',),
                     ('a',), ('a', 'b'), ('b',)]

    assert (res_plan == expected_plan)


def test_union_plans_inverted_some_overlap():
    subplan = [('a',), ('a', 'b', 'c'), ('a', 'c'), ('b',),
               ('b', 'c'), ('c',)]
    full_plan = [('a',), ('a', 'd'), ('b',)]

    res_plan = hs.union_plans(subplan, full_plan)
    expected_plan = [('a',), ('a', 'b', 'c'), ('a', 'c'), ('b',),
                     ('b', 'c'), ('c',), ('a', 'd')]

    assert (res_plan == expected_plan)


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
