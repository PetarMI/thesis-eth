import pytest
import baseline_strategies as bs


###############################################################################
# ############################## BFS ##########################################
###############################################################################
def test_bfs_short():
    nets = ["a", "b"]

    res_plan = bs.bfs(2, nets)
    expected_plan = [
        (), ("a", ), ("b", ), ("a", "b")
    ]

    assert(res_plan == expected_plan)


def test_bfs():
    nets = ['a', 'b', 'c', 'd']

    res_plan = bs.bfs(3, nets)
    expected_plan = [
        (),
        ('a', ), ('b', ), ('c', ), ('d', ),
        ('a', 'b'), ('a', 'c'),  ('a', 'd'),
        ('b', 'c'), ('b', 'd'), ('c', 'd'),
        ('a', 'b', 'c'), ('a', 'b', 'd'),
        ('a', 'c', 'd',), ('b', 'c', 'd')
    ]

    assert(res_plan == expected_plan)


def test_bfs_max():
    nets = ['a', 'b', 'c', 'd']

    res_plan = bs.bfs(4, nets)
    expected_plan = [
        (),
        ('a', ), ('b', ), ('c', ), ('d', ),
        ('a', 'b'), ('a', 'c'),  ('a', 'd'),
        ('b', 'c'), ('b', 'd'), ('c', 'd'),
        ('a', 'b', 'c'), ('a', 'b', 'd'),
        ('a', 'c', 'd',), ('b', 'c', 'd'),
        ('a', 'b', 'c', 'd')
    ]

    assert(res_plan == expected_plan)


def test_bfs_higher_depth():
    nets = ['a', 'b', 'c']

    res_plan = bs.bfs(33, nets)
    expected_plan = [
        (),
        ('a',), ('b',), ('c',),
        ('a', 'b'), ('a', 'c'), ('b', 'c'),
        ('a', 'b', 'c')
    ]

    assert(res_plan == expected_plan)


###############################################################################
# ############################## DFS ##########################################
###############################################################################
def test_dfs_min_depth():
    nets = ['a', 'b', 'c']

    res_plan = bs.dfs(1, nets)
    expected_plan = [
        (), ('a',), ('b',), ('c',)
    ]

    assert (res_plan == expected_plan)


def test_dfs_short():
    nets = ['a', 'b']

    res_plan = bs.dfs(2, nets)
    expected_plan = [
        (), ('a',), ('a', 'b'), ('b',)
    ]

    assert (res_plan == expected_plan)


def test_dfs():
    nets = ['a', 'b', 'c', 'd']

    res_plan = bs.dfs(3, nets)
    expected_plan = [
        (),
        ('a', ), ('a', 'b'), ('a', 'b', 'c'), ('a', 'b', 'd'),
        ('a', 'c'), ('a', 'c', 'd'), ('a', 'd'),
        ('b', ), ('b', 'c'), ('b', 'c', 'd'), ('b', 'd'),
        ('c', ), ('c', 'd'),  ('d', )
    ]

    assert(res_plan == expected_plan)


def test_dfs_max():
    nets = ['a', 'b', 'c', 'd']

    res_plan = bs.dfs(4, nets)
    expected_plan = [
        (),
        ('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'b', 'c', 'd'), ('a', 'b', 'd'),
        ('a', 'c'), ('a', 'c', 'd'), ('a', 'd'),
        ('b',), ('b', 'c'), ('b', 'c', 'd'), ('b', 'd'),
        ('c',), ('c', 'd'), ('d',)
    ]

    assert(res_plan == expected_plan)


def test_dfs_higher_depth():
    nets = ['a', 'b', 'c']

    res_plan = bs.dfs(33, nets)
    expected_plan = [
        (),
        ('a',), ('a', 'b'), ('a', 'b', 'c'), ('a', 'c'),
        ('b',), ('b', 'c'), ('c',)
    ]

    assert(res_plan == expected_plan)
