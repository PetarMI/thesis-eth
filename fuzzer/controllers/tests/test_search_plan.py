import pytest
from Statespace import Statespace


###############################################################################
# ############################## BFS ##########################################
###############################################################################
def test_bfs_stats_short():
    nets = ["a", "b"]

    planner = Statespace(2, nets)
    search_plan = planner.get_bfs_plan()
    res_stats = planner.get_fuzzing_stats()

    expected_stats = {
        "depth0": 1,
        "depth1": 2,
        "depth2": 1,
        "total": 4
    }

    assert(res_stats == expected_stats)
    assert(len(search_plan) == res_stats["total"])


def test_bfs_stats():
    nets = ['a', 'b', 'c', 'd']

    planner = Statespace(3, nets)
    search_plan = planner.get_bfs_plan()
    res_stats = planner.get_fuzzing_stats()

    expected_stats = {
        "depth0": 1,
        "depth1": 4,
        "depth2": 6,
        "depth3": 4,
        "total": 15
    }

    assert(res_stats == expected_stats)
    assert (len(search_plan) == res_stats["total"])


# def test_bfs_stats_large():
#     nets = []
#     for i in range(0, 180):
#         nets.append(str(i))
#
#     planner = Statespace(4, nets)
#     search_plan = planner.get_bfs_plan()
#     res_stats = planner.get_fuzzing_stats()
#
#     expected_stats = {
#         "depth0": 1,
#         "depth1": 180,
#         "depth2": 16110,
#         "depth3": 955860,
#         "depth4": 42296805,
#         "total": 43268956
#     }
#
#     assert(res_stats == expected_stats)
#     assert (len(search_plan) == res_stats["total"])


def test_bfs_stats_max():
    nets = ['a', 'b', 'c', 'd']

    planner = Statespace(4, nets)
    search_plan = planner.get_bfs_plan()
    res_stats = planner.get_fuzzing_stats()

    expected_stats = {
        "depth0": 1,
        "depth1": 4,
        "depth2": 6,
        "depth3": 4,
        "depth4": 1,
        "total": 16
    }

    assert(res_stats == expected_stats)
    assert (len(search_plan) == res_stats["total"])


###############################################################################
# ############################## DFS ##########################################
###############################################################################
def test_dfs_stats_short():
    nets = ["a", "b"]

    planner = Statespace(2, nets)
    search_plan = planner.get_dfs_plan()
    res_stats = planner.get_fuzzing_stats()

    assert (len(search_plan) == 4)
    assert(len(search_plan) == res_stats["total"])


def test_dfs_stats():
    nets = ['a', 'b', 'c', 'd']

    planner = Statespace(3, nets)
    search_plan = planner.get_dfs_plan()
    res_stats = planner.get_fuzzing_stats()

    assert (len(search_plan) == 15)
    assert (len(search_plan) == res_stats["total"])


def test_dfs_stats_max():
    nets = ['a', 'b', 'c', 'd']

    planner = Statespace(4, nets)
    search_plan = planner.get_dfs_plan()
    res_stats = planner.get_fuzzing_stats()

    assert(len(search_plan) == 16)
    assert (len(search_plan) == res_stats["total"])


def test_dfs_stats_large():
    nets = []
    for i in range(0, 100):
        nets.append(str(i))

    planner = Statespace(4, nets)
    search_plan = planner.get_dfs_plan()
    res_stats = planner.get_fuzzing_stats()

    assert (len(search_plan) == res_stats["total"])


###############################################################################
# ############################# COMMON ########################################
###############################################################################
def test_stats_high_k():
    with pytest.raises(ValueError, match="Depth is higher than number of links"):
        nets = ['a', 'b', 'c', 'd']
        Statespace(5, nets)


# def test_stats_unknown_algo():
#     with pytest.raises(ValueError, match="Unknown search algorithm potato"):
#         nets = ['a', 'b', 'c', 'd']
#         planner = Statespace(3, nets)
#         planner.get_search_plan("potato")
