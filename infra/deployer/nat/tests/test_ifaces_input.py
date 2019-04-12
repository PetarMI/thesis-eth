import nat_ifaces
import pytest

# #############################################################################
# ########################## check_same_devices ###############################
# #############################################################################
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


def test_same_devices_fail_empty_orig():
    with pytest.raises(KeyError, match="No devices in orig file"):
        o_ifaces = {}

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

        nat_ifaces.check_same_devices(o_ifaces, s_ifaces)


def test_same_devices_fail_empty_sim():
    with pytest.raises(KeyError, match="No devices in sim file"):
        o_ifaces = {
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

        s_ifaces = {}

        nat_ifaces.check_same_devices(o_ifaces, s_ifaces)


# #############################################################################
# ########################### check_same_length ###############################
# #############################################################################
def test_same_length():
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

    res = nat_ifaces.check_same_length(o_ifaces, s_ifaces)

    assert res


def test_same_length_fail1():
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
            "enp4": "10.0.8.8/24",
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

    res = nat_ifaces.check_same_length(o_ifaces, s_ifaces)

    assert not res


def test_same_length_fail2():
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
            "eth13": "100.18.90.5/24",
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

    res = nat_ifaces.check_same_length(o_ifaces, s_ifaces)

    assert not res


def test_same_length_fail_empty1():
    with pytest.raises(KeyError, match="No interfaces on device topo-r02"):
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
                "eth23": "10.168.90.4/24"
            },
            "topo-r02": {
            },
            "topo-r03": {
                "weth10": "10.45.3.55/24",
            }
        }

        nat_ifaces.check_same_length(o_ifaces, s_ifaces)


def test_same_length_fail_empty2():
    with pytest.raises(KeyError, match="No interfaces on device topo-r02"):
        o_ifaces = {
            "topo-r01": {
                "eth0": "90.4.1.3/24",
                "eth1": "231.3.2.1/24",
                "eth2": "192.168.90.4/24",
            },
            "topo-r02": {
            },
            "topo-r03": {
                "weth0": "115.45.3.55/24",
            }
        }

        s_ifaces = {
            "topo-r01": {
                "eth10": "10.4.1.3/24",
                "eth12": "10.3.2.1/24",
                "eth23": "10.168.90.4/24"
            },
            "topo-r02": {
                "enp0": "45.2.3.1/24",
                "enp1": "85.14.4.4/24",
                "enp2": "122.56.2.1/24",
                "enp3": "92.14.45.8/24",
            },
            "topo-r03": {
                "weth10": "10.45.3.55/24",
            }
        }

        nat_ifaces.check_same_length(o_ifaces, s_ifaces)


# #############################################################################
# ########################### check_same_length ###############################
# #############################################################################
def test_repeated_subnets():
    configs = {
        "topo-r01": {
            "eth0": "10.0.1.2/24",
            "eth1": "10.0.2.2/24",
            "eth2": "10.0.3.2/24",
        },
        "topo-r02": {
            "enp0": "10.0.1.2/24",
            "enp1": "10.0.2.2/24",
            "enp2": "10.0.3.2/24",
            "enp3": "10.0.4.2/24",
        },
        "topo-r03": {
            "weth0": "10.0.1.2/24",
        }
    }

    res = nat_ifaces.check_repeated_subnets(configs)

    assert res


def test_repeated_subnets_weird_ips():
    configs = {
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

    res = nat_ifaces.check_repeated_subnets(configs)

    assert res


def test_repeated_subnets_fail():
    with pytest.raises(ValueError, match="Repeated subnets in device topo-r02"):
        configs = {
            "topo-r01": {
                "eth0": "10.0.1.2/24",
                "eth1": "10.0.2.2/24",
                "eth2": "10.0.3.2/24",
            },
            "topo-r02": {
                "enp0": "10.0.1.2/24",
                "enp1": "10.0.4.5/24",
                "enp2": "10.0.3.2/24",
                "enp3": "10.0.4.2/24",
            },
            "topo-r03": {
                "weth0": "10.0.1.2/24",
            }
        }

        nat_ifaces.check_repeated_subnets(configs)


def test_repeated_subnets_fail2():
    with pytest.raises(ValueError, match="Repeated subnets in device topo-r02"):
        configs = {
            "topo-r01": {
                "eth0": "10.0.1.2/24",
                "eth1": "10.0.2.2/24",
                "eth2": "10.0.3.2/24",
            },
            "topo-r02": {
                "enp0": "10.0.1.2/24",
                "enp1": "10.0.4.5/24",
                "enp2": "10.0.3.2/24",
                "enp3": "10.0.4.2/24",
            },
            "topo-r03": {
                "weth0": "10.0.1.2/24",
                "weth1": "10.0.1.3/24",
            }
        }

        nat_ifaces.check_repeated_subnets(configs)
