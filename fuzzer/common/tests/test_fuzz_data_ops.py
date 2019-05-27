import pytest
import fuzz_data_ops as fdata_ops


###############################################################################
# ############################## VM IP SEARCH #################################
###############################################################################
def test_find_vm_ip_success():
    dev2vm = {
        "r01": "10.0.0.3",
        "r02": "10.0.0.2",
        "r03": "10.0.0.4"
    }

    computed_vm = fdata_ops.find_container_vm('r01', dev2vm)
    expected_vm = "10.0.0.3"

    assert(computed_vm == expected_vm)


def test_find_vm_ip_no_match():
    with pytest.raises(ValueError, match="Container r04 does not exist in dev2vm logs"):
        dev2vm = {
            "r01": "10.0.0.3",
            "r02": "10.0.0.2",
            "r03": "10.0.0.4"
        }

        fdata_ops.find_container_vm('r04', dev2vm)


###############################################################################
# ######################## NETWORK DEVICES SEARCH #############################
###############################################################################
def test_net_devices_success():
    network = "topo-wnet20"

    net2dev = {
        "topo-wnet10": ["topo-r01", "topo-r02"],
        "topo-wnet20": ["topo-r01", "topo-r03"],
        "topo-wnet11": ["topo-r02"],
        "topo-wnet12": ["topo-r02"],
        "topo-wnet21": ["topo-r03"],
        "topo-wnet22": ["topo-r03"]
    }

    res_net_devices = fdata_ops.find_network_devices(network, net2dev)
    expected_net_devices = ["topo-r01", "topo-r03"]

    assert(res_net_devices == expected_net_devices)


def test_net_devices_no_match():
    with pytest.raises(ValueError, match="Network potato does not exist in net2dev logs"):
        network = "potato"

        net2dev = {
            "topo-wnet10": ["topo-r01", "topo-r02"],
            "topo-wnet20": ["topo-r01", "topo-r03"],
            "topo-wnet11": ["topo-r02"],
            "topo-wnet12": ["topo-r02"],
            "topo-wnet21": ["topo-r03"],
            "topo-wnet22": ["topo-r03"]
        }

        fdata_ops.find_network_devices(network, net2dev)


###############################################################################
# ############################# INTERFACE SEARCH ##############################
###############################################################################
def test_find_iface():
    dev_net2iface = {
        "r01": {"wnet1": "eth0", "wnet2": "eth1", "wnet3": "eth2"},
        "r02": {"wnet1": "enp0s1", "wnet4": "enp0s2"},
        "r03": {"wnet1": "weth0", "wnet5": "weth1", "wnet3": "weth2"}
    }

    res_iface = fdata_ops.find_network_interface("r03", "wnet5", dev_net2iface)
    exp_iface = "weth1"

    assert(res_iface == exp_iface)


def test_find_iface2():
    dev_net2iface = {
        "r01": {"wnet1": "eth0", "wnet2": "eth1", "wnet3": "eth2"},
        "r02": {"wnet1": "enp0s1", "wnet4": "enp0s2"},
        "r03": {"wnet1": "weth0", "wnet5": "weth1", "wnet3": "weth2"}
    }

    res_iface = fdata_ops.find_network_interface("r02", "wnet1", dev_net2iface)
    exp_iface = "enp0s1"

    assert(res_iface == exp_iface)


def test_find_iface_no_container():
    with pytest.raises(ValueError, match="Problem with container potato in dev_net2iface logs"):
        dev_net2iface = {
            "r01": {"wnet1": "eth0", "wnet2": "eth1", "wnet3": "eth2"},
            "r02": {"wnet1": "enp0s1", "wnet4": "enp0s2"},
            "r03": {"wnet1": "weth0", "wnet5": "weth1", "wnet3": "weth2"}
        }

        fdata_ops.find_network_interface("potato", "wnet1", dev_net2iface)


def test_find_iface_no_net():
    with pytest.raises(ValueError, match="Problem with network potato on container r01 in dev_net2iface logs"):
        dev_net2iface = {
            "r01": {"wnet1": "eth0", "wnet2": "eth1", "wnet3": "eth2"},
            "r02": {"wnet1": "enp0s1", "wnet4": "enp0s2"},
            "r03": {"wnet1": "weth0", "wnet5": "weth1", "wnet3": "weth2"}
        }

        fdata_ops.find_network_interface("r01", "potato", dev_net2iface)
