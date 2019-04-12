import pytest
import nat_ifaces


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


def test_same_devices():
    o_ifaces = {
        "topo-r01": {
            "eth0": "90.4.1.3/24",
            "eth1": "231.3.2.1/24",
            "eth2": "192.168.90.4/24",
        },
        "topo-r02": {
            "enp0": "45.2.3.1/24",
            "enp1": "85.14.4.4/24",
            "enp2": "122.56.2.1/24",
            "enp3": "92.14.45.8/24",

        },
        "topo-r03": {
            "weth0": "115.45.3.55/24",
        }
    }

    s_ifaces = {
        "topo-r01": {
            "eth10": "10.4.1.3/24",
            "eth12": "10.3.2.1/24",
            "eth23": "10.168.90.4/24",
        },
        "topo-r02": {
            "enp01": "10.2.3.1/24",
            "enp13": "10.14.4.4/24",
            "enp23": "10.56.2.1/24",
            "enp32": "10.14.45.8/24",

        },
        "topo-r03": {
            "weth10": "10.45.3.55/24",
        }
    }

    res = nat_ifaces.check_same_devices(o_ifaces, s_ifaces)

    assert res


def test_same_devices_no_order():
    o_ifaces = {
        "topo-r01": {
            "eth0": "90.4.1.3/24",
            "eth1": "231.3.2.1/24",
            "eth2": "192.168.90.4/24",
        },
        "topo-r02": {
            "enp0": "45.2.3.1/24",
            "enp1": "85.14.4.4/24",
            "enp2": "122.56.2.1/24",
            "enp3": "92.14.45.8/24",

        },
        "topo-r03": {
            "weth0": "115.45.3.55/24",
        }
    }

    s_ifaces = {
        "topo-r02": {
            "enp01": "10.2.3.1/24",
            "enp13": "10.14.4.4/24",
            "enp23": "10.56.2.1/24",
            "enp32": "10.14.45.8/24",

        },
        "topo-r01": {
            "eth10": "10.4.1.3/24",
            "eth12": "10.3.2.1/24",
            "eth23": "10.168.90.4/24",
        },
        "topo-r03": {
            "weth10": "10.45.3.55/24",
        }
    }

    res = nat_ifaces.check_same_devices(o_ifaces, s_ifaces)

    assert res


def test_same_devices_fail1():
    o_ifaces = {
        "topo-r01": {
            "eth0": "90.4.1.3/24",
            "eth1": "231.3.2.1/24",
            "eth2": "192.168.90.4/24",
        },
        "topo-r02": {
            "enp0": "45.2.3.1/24",
            "enp1": "85.14.4.4/24",
            "enp2": "122.56.2.1/24",
            "enp3": "92.14.45.8/24",

        },
        "topo-r03": {
            "weth0": "115.45.3.55/24",
        }
    }

    s_ifaces = {
        "topo-r01": {
            "eth10": "10.4.1.3/24",
            "eth12": "10.3.2.1/24",
            "eth23": "10.168.90.4/24",
        },
        "topo-r04": {
            "enp01": "10.2.3.1/24",
            "enp13": "10.14.4.4/24",
            "enp23": "10.56.2.1/24",
            "enp32": "10.14.45.8/24",

        },
        "topo-r03": {
            "weth10": "10.45.3.55/24",
        }
    }

    res = nat_ifaces.check_same_devices(o_ifaces, s_ifaces)

    assert not res


def test_same_devices_fail2():
    o_ifaces = {
        "topo-r01": {
            "eth0": "90.4.1.3/24",
            "eth1": "231.3.2.1/24",
            "eth2": "192.168.90.4/24",
        },
        "topo-r02": {
            "enp0": "45.2.3.1/24",
            "enp1": "85.14.4.4/24",
            "enp2": "122.56.2.1/24",
            "enp3": "92.14.45.8/24",

        }
    }

    s_ifaces = {
        "topo-r01": {
            "eth10": "10.4.1.3/24",
            "eth12": "10.3.2.1/24",
            "eth23": "10.168.90.4/24",
        },
        "topo-r02": {
            "enp01": "10.2.3.1/24",
            "enp13": "10.14.4.4/24",
            "enp23": "10.56.2.1/24",
            "enp32": "10.14.45.8/24",

        },
        "topo-r03": {
            "weth10": "10.45.3.55/24",
        }
    }

    res = nat_ifaces.check_same_devices(o_ifaces, s_ifaces)

    assert not res
