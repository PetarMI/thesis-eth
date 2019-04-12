import pytest
import nat_ifaces


def test_match_normal():
    orig_ifaces = {
        "topo-r02": {
            "ens6": "20.10.23.1/24",
            "ens7": "20.10.12.2/24"
        },
        "topo-r03": {
            "ens6": "20.10.13.2/24",
            "ens7": "20.10.23.2/24",
            "ens8": "20.10.200.2/24"
        },
        "topo-r01": {
            "ens6": "20.10.100.1/24",
            "ens7": "20.10.12.1/24",
            "ens8": "20.10.13.1/24"
        }
    }

    sim_ifaces = {
        "topo-r02": {
            "ethwe0": "10.0.2.3/24",
            "ethwe1": "10.0.4.2/24"
        },
        "topo-r01": {
            "ethwe0": "10.0.0.2/24",
            "ethwe1": "10.0.2.2/24",
            "ethwe2": "10.0.3.2/24"
        },
        "topo-r03": {
            "ethwe1": "10.0.3.3/24",
            "ethwe0": "10.0.1.2/24",
            "ethwe2": "10.0.4.3/24"
        }
    }

    matched_subnets = {
        "20.10.100.0/24": "10.0.0.0/24",
        "20.10.200.0/24": "10.0.1.0/24",
        "20.10.12.0/24": "10.0.2.0/24",
        "20.10.13.0/24": "10.0.3.0/24",
        "20.10.23.0/24": "10.0.4.0/24"
    }

    matched_ifaces, matched_ips = nat_ifaces.match(orig_ifaces, sim_ifaces, matched_subnets)

    expected_match_ifaces = {
        "topo-r01": {
            "ens6": "ethwe0",
            "ens7": "ethwe1",
            "ens8": "ethwe2"
        },
        "topo-r02": {
            "ens6": "ethwe1",
            "ens7": "ethwe0"
        },
        "topo-r03": {
            "ens6": "ethwe1",
            "ens7": "ethwe2",
            "ens8": "ethwe0"
        }
    }

    expected_match_ips = {
        "topo-r01": {
            "20.10.100.1/24": "10.0.0.2/24",
            "20.10.12.1/24": "10.0.2.2/24",
            "20.10.13.1/24": "10.0.3.2/24"
        },
        "topo-r02": {
            "20.10.12.2/24": "10.0.2.3/24",
            "20.10.23.1/24": "10.0.4.2/24"
        },
        "topo-r03": {
            "20.10.13.2/24": "10.0.3.3/24",
            "20.10.23.2/24": "10.0.4.3/24",
            "20.10.200.2/24": "10.0.1.2/24"
        }
    }

    assert(matched_ifaces == expected_match_ifaces)
    assert(matched_ips == expected_match_ips)


def test_find_sim_subnet_normal():
    o_ip = "216.58.215.238/24"

    matched_subnets = {
        "192.168.10.0/24": "10.0.1.0/24",
        "216.58.215.0/24": "10.0.2.0/24",
        "21.41.21.0/24": "10.0.3.0/24",
        "85.14.4.0/24": "10.0.4.0/24",
        "115.45.3.0/24": "10.0.5.0/24"
    }

    sim_subnet = nat_ifaces.find_sim_subnet(o_ip, matched_subnets)

    assert(sim_subnet == "10.0.2.0/24")


def test_find_sim_subnet_no_match():
    with pytest.raises(ValueError, match="No sim subnet match"):
        o_ip = "216.58.215.238/24"

        matched_subnets = {
            "192.168.10.0/24": "10.0.1.0/24",
            "231.3.2.0/24": "10.0.2.0/24",
            "21.41.21.0/24": "10.0.3.0/24",
            "85.14.4.0/24": "10.0.4.0/24",
            "115.45.3.0/24": "10.0.5.0/24"
        }

        nat_ifaces.find_sim_subnet(o_ip, matched_subnets)


def test_find_sim_config_normal():
    sim_subnet = "10.0.4.0/24"

    sim_config = {
        "eth0": "10.0.1.3/24",
        "eth1": "10.0.2.1/24",
        "eth2": "10.0.3.1/24",
        "eth3": "10.0.4.4/24",
        "eth4": "10.0.5.5/24",
        "eth5": "10.0.6.2/24",
        "eth6": "10.0.7.3/24"
    }

    sim_iface, sim_ip = nat_ifaces.find_sim_config(sim_subnet, sim_config)
    assert (sim_iface == "eth3")
    assert (sim_ip == "10.0.4.4/24")


def test_find_sim_config_weird_ifaces():
    sim_subnet = "85.14.4.0/24"

    sim_config = {
        "eth0": "90.4.1.3/24",
        "enps1": "45.2.3.1/24",
        "eth3": "231.3.2.1/24",
        "weth1": "85.14.4.4/24",
        "enps8": "122.56.2.1/24",
        "enps9": "192.168.90.4/24",
        "enp9s8": "115.45.3.55/24",
    }

    sim_iface, sim_ip = nat_ifaces.find_sim_config(sim_subnet, sim_config)
    assert (sim_iface == "weth1")
    assert (sim_ip == "85.14.4.4/24")


def test_find_sim_config_no_match():
    with pytest.raises(ValueError, match="No sim IP match"):
        sim_subnet = "10.0.69.0/24"

        sim_config = {
            "eth0": "10.0.1.3/24",
            "eth1": "10.0.2.1/24",
            "eth2": "10.0.3.1/24",
            "eth3": "10.0.4.4/24",
            "eth4": "10.0.5.5/24",
            "eth5": "10.0.6.2/24",
            "eth6": "10.0.7.3/24"
        }

        nat_ifaces.find_sim_config(sim_subnet, sim_config)


def test_find_sim_config_multiple_match():
    with pytest.raises(ValueError, match="Multiple sim IP match"):
        sim_subnet = "10.0.2.0/24"

        sim_config = {
            "eth0": "10.0.1.3/24",
            "eth1": "10.0.2.1/24",
            "eth2": "10.0.3.1/24",
            "eth3": "10.0.4.4/24",
            "eth4": "10.0.2.5/24",
            "eth5": "10.0.6.2/24",
            "eth6": "10.0.7.3/24"
        }

        nat_ifaces.find_sim_config(sim_subnet, sim_config)
