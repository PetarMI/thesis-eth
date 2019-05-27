import pytest
import FuzzData as fd


###############################################################################
# ####################### Networks to devices #################################
###############################################################################
def test_net2dev_exact():
    containers = [
        {
            "name": "r01",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet12"},
                           {"network": "wnet13"},
                           {"network": "wnet14"}]
        },
        {
            "name": "r02",
            "interfaces": [{"network": "wnet20"},
                           {"network": "wnet12"},
                           {"network": "wnet23"},
                           {"network": "wnet24"}]
        },
        {
            "name": "r03",
            "interfaces": [{"network": "wnet30"},
                           {"network": "wnet13"},
                           {"network": "wnet23"},
                           {"network": "wnet34"}]
        },
        {
            "name": "r04",
            "interfaces": [{"network": "wnet40"},
                           {"network": "wnet14"},
                           {"network": "wnet24"},
                           {"network": "wnet34"}]
        }
    ]

    res_net2dev = fd.parse_net2devices(containers, "topo")
    expected_net2dev = {
        "topo-wnet10": ["topo-r01"],
        "topo-wnet20": ["topo-r02"],
        "topo-wnet30": ["topo-r03"],
        "topo-wnet40": ["topo-r04"],
        "topo-wnet12": ["topo-r01", "topo-r02"],
        "topo-wnet13": ["topo-r01", "topo-r03"],
        "topo-wnet14": ["topo-r01", "topo-r04"],
        "topo-wnet23": ["topo-r02", "topo-r03"],
        "topo-wnet24": ["topo-r02", "topo-r04"],
        "topo-wnet34": ["topo-r03", "topo-r04"],
    }

    assert (res_net2dev == expected_net2dev)


def test_net2dev_part():
    containers = [
        {
            "name": "r01",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet20"}]
        },
        {
            "name": "r02",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet11"},
                           {"network": "wnet12"}]
        },
        {
            "name": "r03",
            "interfaces": [{"network": "wnet20"},
                           {"network": "wnet21"},
                           {"network": "wnet22"}]
        }
    ]

    res_net2dev = fd.parse_net2devices(containers, "topo")
    expected_net2dev = {
        "topo-wnet10": ["topo-r01", "topo-r02"],
        "topo-wnet20": ["topo-r01", "topo-r03"],
        "topo-wnet11": ["topo-r02"],
        "topo-wnet12": ["topo-r02"],
        "topo-wnet21": ["topo-r03"],
        "topo-wnet22": ["topo-r03"]
    }

    assert(res_net2dev == expected_net2dev)


def test_net2dev_empty():
    containers: list = []

    res_net2dev = fd.parse_net2devices(containers, "topo")
    expected_net2dev = {}

    assert(res_net2dev == expected_net2dev)


def test_net2dev_many_conns():
    with pytest.raises(ValueError, match="More than two containers connected to network topo-wnet10"):
        containers = [
            {
                "name": "r01",
                "interfaces": [{"network": "wnet10"},
                               {"network": "wnet20"}]
            },
            {
                "name": "r02",
                "interfaces": [{"network": "wnet10"},
                               {"network": "wnet11"},
                               {"network": "wnet12"}]
            },
            {
                "name": "r03",
                "interfaces": [{"network": "wnet20"},
                               {"network": "wnet21"},
                               {"network": "wnet22"},
                               {"network": "wnet10"}]
            }
        ]

        fd.parse_net2devices(containers, "topo")


###############################################################################
# ########################### Devices to VMs ##################################
###############################################################################
def test_dev2vm_exact():
    containers = [
            {"name": "r01", "vm": "0"},
            {"name": "r02", "vm": "1"},
            {"name": "r03", "vm": "2"}
        ]

    vms = {
        "0": {"ip": "10.0.0.1"},
        "1": {"ip": "10.0.0.2"},
        "2": {"ip": "10.0.0.3"}
    }

    res_dev2vm = fd.parse_dev2vm(containers, vms, "topo")
    expected_dev2vm = {
        "topo-r01": "10.0.0.1",
        "topo-r02": "10.0.0.2",
        "topo-r03": "10.0.0.3",
    }

    assert(res_dev2vm == expected_dev2vm)


def test_dev2vm_more_vms():
    containers = [
            {"name": "r01", "vm": "0"},
            {"name": "r02", "vm": "5"},
            {"name": "r03", "vm": "4"}
        ]

    vms = {
        "0": {"ip": "10.0.0.1"},
        "1": {"ip": "10.0.0.2"},
        "2": {"ip": "10.0.0.3"},
        "3": {"ip": "10.0.0.4"},
        "4": {"ip": "10.0.0.5"},
        "5": {"ip": "10.0.0.6"}

    }

    res_dev2vm = fd.parse_dev2vm(containers, vms, "topo")
    expected_dev2vm = {
        "topo-r01": "10.0.0.1",
        "topo-r02": "10.0.0.6",
        "topo-r03": "10.0.0.5"
    }

    assert(res_dev2vm == expected_dev2vm)


def test_dev2vm_less_vms():
    containers = [
            {"name": "r01", "vm": "0"},
            {"name": "r02", "vm": "0"},
            {"name": "r03", "vm": "1"}
        ]

    vms = {
        "0": {"ip": "10.0.0.1"},
        "1": {"ip": "10.0.0.2"}

    }

    res_dev2vm = fd.parse_dev2vm(containers, vms, "topo")
    expected_dev2vm = {
        "topo-r01": "10.0.0.1",
        "topo-r02": "10.0.0.1",
        "topo-r03": "10.0.0.2"
    }

    assert(res_dev2vm == expected_dev2vm)


def test_dev2vm_repeated():
    containers = [
            {"name": "r01", "vm": "3"},
            {"name": "r02", "vm": "2"},
            {"name": "r03", "vm": "4"},
            {"name": "r04", "vm": "2"}
        ]

    vms = {
        "2": {"ip": "10.0.0.2"},
        "3": {"ip": "10.0.0.3"},
        "4": {"ip": "10.0.0.4"}

    }

    res_dev2vm = fd.parse_dev2vm(containers, vms, "topo")
    expected_dev2vm = {
        "topo-r01": "10.0.0.3",
        "topo-r02": "10.0.0.2",
        "topo-r03": "10.0.0.4",
        "topo-r04": "10.0.0.2"
    }

    assert(res_dev2vm == expected_dev2vm)


def test_dev2vm_no_vm():
    with pytest.raises(ValueError, match="No running vm with id 4"):
        containers = [
                {"name": "r01", "vm": "0"},
                {"name": "r02", "vm": "4"}
            ]

        vms = {
            "0": {"ip": "10.0.0.1"},
            "1": {"ip": "10.0.0.2"},
            "2": {"ip": "10.0.0.3"}
        }

        fd.parse_dev2vm(containers, vms, "topo")


def test_dev2vm_no_vm_empty():
    with pytest.raises(ValueError, match="No running vm with id 0"):
        containers = [
                {"name": "r01", "vm": "0"},
                {"name": "r02", "vm": "4"}
            ]

        vms = {}

        fd.parse_dev2vm(containers, vms, "topo")


###############################################################################
# ######################### Parse nets to ifaces ##############################
###############################################################################
def test_net2iface():
    sim_ifaces = {
        "r01": {
            "10.0.10.5/24": "eth0",
            "10.0.12.6/24": "eth1"
        },
        "r02": {
            "10.0.20.5/24": "eth0",
            "10.0.12.7/24": "eth1",
            "10.0.23.6/24": "eth2",
            "10.0.24.6/24": "eth3"
        },
        "r03": {
            "10.0.30.5/24": "eth0",
            "10.0.23.5/24": "eth1",
            "10.0.34.6/24": "eth2"
        }

    }

    sim_nets = {
        "10.0.10.0/24": "net1",
        "10.0.20.0/24": "net2",
        "10.0.30.0/24": "net3",
        "10.0.12.0/24": "net4",
        "10.0.23.0/24": "net5",
        "10.0.24.0/24": "net6",
        "10.0.34.0/24": "net7"
    }

    res_parse = fd.parse_nets2ifaces(sim_ifaces, sim_nets)
    expected_parse = {
        "r01": {
            "net1": "eth0",
            "net4": "eth1",
        },
        "r02": {
            "net2": "eth0",
            "net4": "eth1",
            "net5": "eth2",
            "net6": "eth3"
        },
        "r03": {
            "net3": "eth0",
            "net5": "eth1",
            "net7": "eth2"
        }
    }

    assert(res_parse == expected_parse)


###############################################################################
# #################### Match single device ifaces #############################
###############################################################################
def test_match_ifaces_exact():
    dev_sim_ifaces = {
        "10.0.0.5/24": "eth0",
        "10.0.1.6/24": "eth1",
        "10.0.2.7/24": "eth2"
    }

    sim_nets = {
        "10.0.0.0/24": "net1",
        "10.0.1.0/24": "net2",
        "10.0.2.0/24": "net3"
    }

    res_match = fd.match_dev_net2iface(dev_sim_ifaces, sim_nets)
    expected_match = {
        "net1": "eth0",
        "net2": "eth1",
        "net3": "eth2",
    }

    assert(res_match == expected_match)


def test_match_ifaces_more_nets():
    dev_sim_ifaces = {
        "10.0.4.5/24": "eth0",
        "10.0.2.6/24": "eth1"
    }

    sim_nets = {
        "10.0.0.0/24": "net1",
        "10.0.1.0/24": "net2",
        "10.0.2.0/24": "net3",
        "10.0.3.0/24": "net4",
        "10.0.4.0/24": "net5"
    }

    res_match = fd.match_dev_net2iface(dev_sim_ifaces, sim_nets)
    expected_match = {
        "net5": "eth0",
        "net3": "eth1"
    }

    assert(res_match == expected_match)


def test_match_ifaces_no_net():
    with pytest.raises(ValueError, match="Network 10.0.2.0/24 does not exist"):
        dev_sim_ifaces = {
            "10.0.1.5/24": "eth0",
            "10.0.2.6/24": "eth1"
        }

        sim_nets = {
            "10.0.0.0/24": "net1",
            "10.0.1.0/24": "net2"
        }

        fd.match_dev_net2iface(dev_sim_ifaces, sim_nets)


def test_match_ifaces_empty_nets():
    with pytest.raises(ValueError, match="Network 10.0.1.0/24 does not exist"):
        dev_sim_ifaces = {
            "10.0.1.5/24": "eth0",
            "10.0.2.6/24": "eth1"
        }

        sim_nets = {}

        fd.match_dev_net2iface(dev_sim_ifaces, sim_nets)


###############################################################################
# ############################# Check None ####################################
###############################################################################
def test_check_none_none():
    with pytest.raises(ValueError, match="Test"):
        fd.check_none(None, "Test")


def test_check_none_dict():
    with pytest.raises(ValueError, match="Test"):
        fd.check_none(dict(), "Test")


def test_check_none_list():
    with pytest.raises(ValueError, match="Test"):
        fd.check_none([], "Test")


def test_check_none_str():
    with pytest.raises(ValueError, match="Test"):
        fd.check_none("", "Test")
