import pytest
import fuzz_data_ops as fdata_ops

###############################################################################
# ############################## VM IP SEARCH #################################
###############################################################################
def test_get_vm_ip_success():
    containers = {
        'r01': {
            'vm': '0',
            'interfaces': [
                {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
            ]
        },
        'r02': {
            'vm': '1',
            'interfaces': [
                {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
            ]
        },
        'r03': {
            'vm': '1',
            'interfaces': [
                {'network': 'wnet200', 'ipaddr': '20.10.200.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.3'}
            ]
        }
    }

    vms = {
        '0': {
            'ip': '192.168.56.10',
            'role': 'manager'},
        '1': {
            'ip': '192.168.56.11',
            'role': 'worker'}
    }

    computed_vm = fdata_ops.find_container_vm('r01', containers, vms)
    expected_vm = "192.168.56.10"

    assert(computed_vm == expected_vm)


def test_get_vm_ip_success2():
    containers = {
        'r01': {
            'vm': '0',
            'interfaces': [
                {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
            ]
        },
        'r02': {
            'vm': '1',
            'interfaces': [
                {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
            ]
        },
        'r03': {
            'vm': '1',
            'interfaces': [
                {'network': 'wnet200', 'ipaddr': '20.10.200.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.3'}
            ]
        }
    }

    vms = {
        '0': {
            'ip': '192.168.56.10',
            'role': 'manager'},
        '1': {
            'ip': '192.168.56.11',
            'role': 'worker'}
    }

    computed_vm = fdata_ops.find_container_vm('r03', containers, vms)
    expected_vm = "192.168.56.11"

    assert(computed_vm == expected_vm)


def test_get_vm_ip_no_src():
    with pytest.raises(ValueError, match="Property src container r04 not in topo file"):
        containers = {
            'r01': {
                'vm': '0',
                'interfaces': [
                    {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                    {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                    {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
                ]
            },
            'r02': {
                'vm': '1',
                'interfaces': [
                    {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                    {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
                ]
            }
        }

        vms = {}

        fdata_ops.find_container_vm('r04', containers, vms)


def test_get_vm_ip_no_src_empty_cont():
    with pytest.raises(ValueError, match="Property src container r01 not in topo file"):
        containers = {}
        vms = {}

        fdata_ops.find_container_vm('r01', containers, vms)


def test_get_vm_ip_no_vm_with_id():
    with pytest.raises(ValueError, match="No running VM with ID 4"):
        containers = {
            'r01': {
                'vm': '4',
                'interfaces': [
                    {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                    {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                    {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
                ]
            },
            'r02': {
                'vm': '1',
                'interfaces': [
                    {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                    {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
                ]
            }
        }

        vms = {
            '0': {
                'ip': '192.168.56.10',
                'role': 'manager'},
            '1': {
                'ip': '192.168.56.11',
                'role': 'worker'}
        }

        fdata_ops.find_container_vm('r01', containers, vms)


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
    with pytest.raises(ValueError, match="Network potato does not exist in fuzzing data logs"):
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
