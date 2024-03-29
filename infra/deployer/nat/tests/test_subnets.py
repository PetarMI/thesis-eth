import pytest
import nat_subnets


def test_matching_success():
    orig_subnets = {
        "net1": "151.101.128.0/24",
        "net2": "151.101.140.0/24",
        "net3": "151.101.120.0/24",
        "net4": "151.101.135.0/24",
        "net5": "151.101.119.0/24"
    }

    sim_subnets = {
        "net1": "10.0.1.0/24",
        "net2": "10.0.2.0/24",
        "net3": "10.0.3.0/24",
        "net4": "10.0.4.0/24",
        "net5": "10.0.5.0/24"
    }

    matched_subnets = nat_subnets.match_subnets(orig_subnets, sim_subnets)
    expected_match = {
        "151.101.128.0/24": "10.0.1.0/24",
        "151.101.140.0/24": "10.0.2.0/24",
        "151.101.120.0/24": "10.0.3.0/24",
        "151.101.135.0/24": "10.0.4.0/24",
        "151.101.119.0/24": "10.0.5.0/24"
    }

    assert(matched_subnets == expected_match)


def test_matching_success_similar():
    orig_subnets = {
        "net1": "151.101.128.0/24",
        "net2": "151.101.140.0/24",
        "net3": "10.0.0.0/24",
        "net4": "10.0.0.2/24",
        "net5": "10.0.0.4/24"
    }

    sim_subnets = {
        "net1": "10.0.1.0/24",
        "net2": "10.0.2.0/24",
        "net3": "10.0.3.0/24",
        "net4": "10.0.4.0/24",
        "net5": "10.0.5.0/24"
    }

    matched_subnets = nat_subnets.match_subnets(orig_subnets, sim_subnets)
    expected_match = {
        "151.101.128.0/24": "10.0.1.0/24",
        "151.101.140.0/24": "10.0.2.0/24",
        "10.0.0.0/24": "10.0.3.0/24",
        "10.0.0.2/24": "10.0.4.0/24",
        "10.0.0.4/24": "10.0.5.0/24"
    }

    assert(matched_subnets == expected_match)


def test_matching_success_similar2():
    orig_subnets = {
        "net1": "151.101.128.0/24",
        "net2": "151.101.140.0/24",
        "net3": "10.0.0.0/24",
        "net4": "10.0.0.2/24",
        "net5": "10.0.0.4/24"
    }

    sim_subnets = {
        "net1": "10.0.0.0/24",
        "net2": "10.0.1.0/24",
        "net3": "10.0.2.0/24",
        "net4": "10.0.3.0/24",
        "net5": "10.0.4.0/24"
    }

    matched_subnets = nat_subnets.match_subnets(orig_subnets, sim_subnets)
    expected_match = {
        "151.101.128.0/24": "10.0.0.0/24",
        "151.101.140.0/24": "10.0.1.0/24",
        "10.0.0.0/24": "10.0.2.0/24",
        "10.0.0.2/24": "10.0.3.0/24",
        "10.0.0.4/24": "10.0.4.0/24"
    }

    assert(matched_subnets == expected_match)


def test_matching_success_similar3():
    orig_subnets = {
        "net1": "151.101.128.0/24",
        "net2": "151.101.140.0/24",
        "net3": "10.0.0.0/31",
        "net4": "10.0.0.2/31",
        "net5": "10.0.0.4/31"
    }

    sim_subnets = {
        "net1": "10.0.0.0/24",
        "net2": "10.0.1.0/24",
        "net3": "10.0.2.0/24",
        "net4": "10.0.3.0/24",
        "net5": "10.0.4.0/24"
    }

    matched_subnets = nat_subnets.match_subnets(orig_subnets, sim_subnets)
    expected_match = {
        "151.101.128.0/24": "10.0.0.0/24",
        "151.101.140.0/24": "10.0.1.0/24",
        "10.0.0.0/31": "10.0.2.0/24",
        "10.0.0.2/31": "10.0.3.0/24",
        "10.0.0.4/31": "10.0.4.0/24"
    }

    assert(matched_subnets == expected_match)


def test_matching_diff_lengths1():
    with pytest.raises(KeyError, match="Network number mismatch"):
        orig_subnets = {
            "net1": "151.101.128.0/24",
            "net2": "151.101.140.0/24",
            "net3": "151.101.120.0/24",
            "net4": "151.101.135.0/24",
            "net5": "151.101.119.0/24"
        }

        sim_subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        nat_subnets.validate_subnets(orig_subnets, sim_subnets)


def test_matching_diff_lengths2():
    with pytest.raises(KeyError, match="Network number mismatch"):
        orig_subnets = {
            "net1": "151.101.128.0/24",
            "net2": "151.101.140.0/24",
            "net4": "151.101.135.0/24",
            "net5": "151.101.119.0/24"
        }

        sim_subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        nat_subnets.validate_subnets(orig_subnets, sim_subnets)


def test_diff_subnets():
    with pytest.raises(KeyError, match="Network mismatch"):
        orig_subnets = {
            "net1": "151.101.128.0/24",
            "net2": "151.101.140.0/24",
            "net3": "151.101.120.0/24",
            "net44": "151.101.135.0/24",
            "net5": "151.101.119.0/24"
        }

        sim_subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        nat_subnets.validate_subnets(orig_subnets, sim_subnets)


def test_parse_subnets_success():
    nets = [
        {"name": "wnet100", "subnet": "20.10.100.0/24"},
        {"name": "wnet200", "subnet": "20.10.200.0/24"},
        {"name": "wnet12",  "subnet": "20.10.12.0/24"},
        {"name": "wnet13",  "subnet": "20.10.13.0/24"},
        {"name": "wnet23",  "subnet": "20.10.23.0/24"}
    ]

    topo_name = "sirene"

    subnets = nat_subnets.parse_orig_subnets(topo_name, nets)

    expected_subnets = {
        "sirene-wnet100": "20.10.100.0/24",
        "sirene-wnet200": "20.10.200.0/24",
        "sirene-wnet12": "20.10.12.0/24",
        "sirene-wnet13": "20.10.13.0/24",
        "sirene-wnet23": "20.10.23.0/24",
    }

    assert(subnets == expected_subnets)


def test_parse_subnets_success_weirder():
    nets = [
        {"name": "wnet100", "subnet": "100.10.100.0/24"},
        {"name": "wnet200", "subnet": "100.10.200.0/24"},
        {"name": "wnet12",  "subnet": "10.0.0.0/31"},
        {"name": "wnet13",  "subnet": "10.0.0.2/31"},
        {"name": "wnet23",  "subnet": "10.0.0.4/31"}
    ]

    topo_name = "sirene"

    subnets = nat_subnets.parse_orig_subnets(topo_name, nets)

    expected_subnets = {
        "sirene-wnet100": "100.10.100.0/24",
        "sirene-wnet200": "100.10.200.0/24",
        "sirene-wnet12": "10.0.0.0/31",
        "sirene-wnet13": "10.0.0.2/31",
        "sirene-wnet23": "10.0.0.4/31",
    }

    assert(subnets == expected_subnets)


def test_parse_subnets_duplicate_name():
    with pytest.raises(KeyError, match="Duplicate subnet"):
        nets = [
            {"name": "wnet100", "subnet": "20.10.100.0/24"},
            {"name": "wnet200", "subnet": "20.10.200.0/24"},
            {"name": "wnet100",  "subnet": "20.10.12.0/24"},
            {"name": "wnet13",  "subnet": "20.10.13.0/24"},
            {"name": "wnet23",  "subnet": "20.10.23.0/24"}
        ]

        topo_name = "sirene"

        nat_subnets.parse_orig_subnets(topo_name, nets)


def test_update_name():
    topo_name = "sirene"
    orig_net_name = "inet100"

    sim_name = nat_subnets.update_net_name(topo_name, orig_net_name)

    assert(sim_name == "sirene-inet100")
