import search_strategies as ss


def test_bfs_short():
    nets = ["a", "b"]

    res_plan = ss.bfs(2, nets)
    expected_plan = [
        (), ("a", ), ("b", ), ("a", "b")
    ]

    assert(res_plan == expected_plan)


def test_bfs():
    nets = ['a', 'b', 'c', 'd']

    res_plan = ss.bfs(3, nets)
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

    res_plan = ss.bfs(4, nets)
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

    res_plan = ss.bfs(33, nets)
    expected_plan = [
        (),
        ('a',), ('b',), ('c',),
        ('a', 'b'), ('a', 'c'), ('b', 'c'),
        ('a', 'b', 'c')
    ]

    assert(res_plan == expected_plan)
