from fuzzer.Fuzzer import Fuzzer
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


def get_search_strategy():
    fuzzer = Fuzzer()
    fuzzer.prepare_fuzzing(3, "bfs")
    bfs_plan = fuzzer.get_search_plan()
    print(bfs_plan)

    fuzzer.prepare_fuzzing(3, "dfs")
    dfs_plan = fuzzer.get_search_plan()
    print(dfs_plan)

    assert(len(bfs_plan) == len(dfs_plan))

    return bfs_plan, dfs_plan


def calc_fr_ops(search_plan: list):
    drops = 0
    restores = 0

    last_state = ()

    for state in search_plan:
        restores += len(last_state)
        drops += len(state)

        last_state = state

    return drops, restores


def calc_pr_ops(search_plan: list):
    drops = 0
    restores = 0

    last_state = ()

    for state in search_plan:
        restores += len(state_diff(last_state, state))
        drops += len(state_diff(state, last_state))

        last_state = state

    return drops, restores


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


def compare_num_ops():
    bfs_plan, dfs_plan = get_search_strategy()

    bfs_ds, bfs_rs = calc_fr_ops(bfs_plan)
    dfs_ds, dfs_rs = calc_fr_ops(dfs_plan)

    write_results("full", bfs_ds, bfs_rs, dfs_ds, dfs_rs)

    print("Full revert:")
    print("BFS drops vs DFS drops = {} : {}".format(bfs_ds, dfs_ds))
    print("BFS restores vs DFS restores = {} : {}".format(bfs_rs, dfs_rs))
    print()

    bfs_ds, bfs_rs = calc_pr_ops(bfs_plan)
    dfs_ds, dfs_rs = calc_pr_ops(dfs_plan)

    write_results("partial", bfs_ds, bfs_rs, dfs_ds, dfs_rs)

    print("Partial revert:")
    print("BFS drops vs DFS drops = {} : {}".format(bfs_ds, dfs_ds))
    print("BFS restores vs DFS restores = {} : {}".format(bfs_rs, dfs_rs))


def write_results(op, bfs_ds, bfs_rs, dfs_ds, dfs_rs):
    with open(const.REVERT_STATS, "a") as logfile:
        logfile.write("{},{},{},{},{}\n".format(op, bfs_ds, bfs_rs, dfs_ds, dfs_rs))


compare_num_ops()
