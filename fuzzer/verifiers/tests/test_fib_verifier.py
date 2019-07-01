import reach_fib_verifier as rfv


def test_next_hop_ok():
    next_hop = "10.0.3.2"
    failed_nets = ["10.0.1.0/24", "10.0.2.0/24"]

    res = rfv.check_next_hop_failed(next_hop, failed_nets)

    assert(res is False)


def test_next_hop_ok_complex():
    next_hop = "10.0.3.2"
    failed_nets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.128/25"]

    res = rfv.check_next_hop_failed(next_hop, failed_nets)

    assert(res is False)


def test_next_hop_failed():
    next_hop = "10.0.3.2"
    failed_nets = ["10.0.1.0/24", "10.0.2.0/24",
                   "10.0.3.0/24", "10.0.5.0/24"]

    res = rfv.check_next_hop_failed(next_hop, failed_nets)

    assert res


def test_next_hop_failed_complex():
    next_hop = "10.0.3.2"
    failed_nets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/25"]

    res = rfv.check_next_hop_failed(next_hop, failed_nets)

    assert res
