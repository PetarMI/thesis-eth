from fuzzer import Fuzzer


def test_conv_param_parse():
    link_changes = {
        "drop": ["10.0.1.0/24", "10.0.2.0/24"],
        "restore": ["10.0.3.0/24", "10.0.4.0/24"]
    }

    res_params = Fuzzer.parse_convergence_links(link_changes)
    expected_params = ["-d", "10.0.1.0/24,10.0.2.0/24",
                       "-r", "10.0.3.0/24,10.0.4.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_restored():
    link_changes = {
        "drop": ["10.0.1.0/24", "10.0.2.0/24"],
        "restore": []
    }

    res_params = Fuzzer.parse_convergence_links(link_changes)
    expected_params = ["-d", "10.0.1.0/24,10.0.2.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_dropped():
    link_changes = {
        "restore": ["10.0.1.0/24", "10.0.2.0/24"],
        "drop": []
    }

    res_params = Fuzzer.parse_convergence_links(link_changes)
    expected_params = ["-r", "10.0.1.0/24,10.0.2.0/24"]

    assert(res_params == expected_params)


def test_conv_param_parse_no_changes():
    link_changes = {
        "restore": [],
        "drop": []
    }

    res_params = Fuzzer.parse_convergence_links(link_changes)
    expected_params = []

    assert(res_params == expected_params)

