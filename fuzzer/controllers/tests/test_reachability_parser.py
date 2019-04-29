import pytest
import reachability_parser as rp


def test_get_vm_ip_success():
    prop = {'src': 'r01', 'dest': '20.10.200.2'}

    containers = [
        {
            'name': 'r01',
            'type': 'frr',
            'vm': '0',
            'interfaces': [
                {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
            ]
        },
        {
            'name': 'r02',
            'type': 'frr',
            'vm': '1',
            'interfaces': [
                {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
            ]
        },
        {
            'name': 'r03',
            'type': 'frr',
            'vm': '1',
            'interfaces': [
                {'network': 'wnet200', 'ipaddr': '20.10.200.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.3'}
            ]
        }
    ]

    vms = {
        '0': {
            'ip': '192.168.56.10',
            'role': 'manager'},
        '1': {
            'ip': '192.168.56.11',
            'role': 'worker'}
    }

    computed_vm = rp.get_vm_ip(prop, containers, vms)
    expected_vm = "192.168.56.10"

    assert(computed_vm == expected_vm)


def test_get_vm_ip_success2():
    prop = {'src': 'r03', 'dest': '20.10.200.2'}

    containers = [
        {
            'name': 'r01',
            'type': 'frr',
            'vm': '0',
            'interfaces': [
                {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
            ]
        },
        {
            'name': 'r02',
            'type': 'frr',
            'vm': '1',
            'interfaces': [
                {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
            ]
        },
        {
            'name': 'r03',
            'type': 'frr',
            'vm': '1',
            'interfaces': [
                {'network': 'wnet200', 'ipaddr': '20.10.200.2'},
                {'network': 'wnet13', 'ipaddr': '20.10.13.3'},
                {'network': 'wnet23', 'ipaddr': '20.10.23.3'}
            ]
        }
    ]

    vms = {
        '0': {
            'ip': '192.168.56.10',
            'role': 'manager'},
        '1': {
            'ip': '192.168.56.11',
            'role': 'worker'}
    }

    computed_vm = rp.get_vm_ip(prop, containers, vms)
    expected_vm = "192.168.56.11"

    assert(computed_vm == expected_vm)


def test_get_vm_ip_no_src():
    with pytest.raises(ValueError, match="Property src container r04 not in topo file"):
        prop = {'src': 'r04', 'dest': '20.10.200.2'}

        containers = [
            {
                'name': 'r01',
                'type': 'frr',
                'vm': '0',
                'interfaces': [
                    {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                    {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                    {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
                ]
            },
            {
                'name': 'r02',
                'type': 'frr',
                'vm': '1',
                'interfaces': [
                    {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                    {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
                ]
            }
        ]

        vms = {}

        rp.get_vm_ip(prop, containers, vms)


def test_get_vm_ip_no_src_empty_cont():
    with pytest.raises(ValueError, match="Property src container r01 not in topo file"):
        prop = {'src': 'r01', 'dest': '20.10.200.2'}

        containers = []
        vms = {}

        rp.get_vm_ip(prop, containers, vms)


def test_get_vm_ip_no_vm_with_id():
    with pytest.raises(ValueError, match="No running VM with ID 4"):
        prop = {'src': 'r01', 'dest': '20.10.200.2'}

        containers = [
            {
                'name': 'r01',
                'type': 'frr',
                'vm': '4',
                'interfaces': [
                    {'network': 'wnet100', 'ipaddr': '20.10.100.1'},
                    {'network': 'wnet12', 'ipaddr': '20.10.12.2'},
                    {'network': 'wnet13', 'ipaddr': '20.10.13.2'}
                ]
            },
            {
                'name': 'r02',
                'type': 'frr',
                'vm': '1',
                'interfaces': [
                    {'network': 'wnet12', 'ipaddr': '20.10.12.3'},
                    {'network': 'wnet23', 'ipaddr': '20.10.23.2'}
                ]
            }
        ]

        vms = {
            '0': {
                'ip': '192.168.56.10',
                'role': 'manager'},
            '1': {
                'ip': '192.168.56.11',
                'role': 'worker'}
        }

        rp.get_vm_ip(prop, containers, vms)
