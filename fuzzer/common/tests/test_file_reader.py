from fuzzer.common import file_reader as fr


def test_swap_order_yes():
    a = "cl"
    b = "uel"

    res_a, res_b = fr.swap_order(a, b, swap=True)

    assert(res_a == "uel")
    assert (res_b == "cl")
    # also test that it is not doing anything to the original values
    assert(a == "cl")
    assert(b == "uel")


def test_swap_order_no():
    a = "cl"
    b = "uel"

    res_a, res_b = fr.swap_order(a, b, swap=False)

    assert(res_a == "cl")
    assert (res_b == "uel")
    # also test that it is not doing anything to the original values
    assert(a == "cl")
    assert(b == "uel")
