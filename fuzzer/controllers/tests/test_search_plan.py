import pytest
from Statespace import SearchPlan


def test_stats_short():
    nets = ["a", "b"]

    planner = SearchPlan(2, nets)
    search_plan = planner.get_search_plan("bfs")
    res_stats = planner.get_fuzzing_stats()

    expected_stats = {
        "depth0": 1,
        "depth1": 2,
        "depth2": 1,
        "total": 4
    }

    assert(res_stats == expected_stats)
    assert(len(search_plan) == res_stats["total"])


def test_stats():
    nets = ['a', 'b', 'c', 'd']

    planner = SearchPlan(3, nets)
    search_plan = planner.get_search_plan("bfs")
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


# def test_stats_large():
#     nets = []
#     for i in range(0, 180):
#         nets.append(str(i))
#
#     planner = SearchPlan(4, nets)
#     search_plan = planner.get_search_plan("bfs")
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


def test_stats_max():
    nets = ['a', 'b', 'c', 'd']

    planner = SearchPlan(4, nets)
    search_plan = planner.get_search_plan("bfs")
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


def test_stats_high_k():
    with pytest.raises(ValueError, match="Depth is higher than number of nets"):
        nets = ['a', 'b', 'c', 'd']
        SearchPlan(5, nets)


def test_stats_unknown_algo():
    with pytest.raises(ValueError, match="Unknown search algorithm potato"):
        nets = ['a', 'b', 'c', 'd']
        planner = SearchPlan(3, nets)
        planner.get_search_plan("potato")
