import ipaddress
import pytest
import net_validator


# #############################################################################
# ############################# SUBNETS #######################################
# #############################################################################
def test_valid_subnets_success():
    subnets = {
        "net1": "10.0.1.0/24",
        "net2": "10.0.2.0/24",
        "net3": "10.0.3.0/24",
        "net4": "10.0.4.0/24",
        "net5": "10.0.5.0/24"
    }

    net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_invalid_ip():
    with pytest.raises(ipaddress.AddressValueError):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.413.0/24",
            "net5": "10.0.5.0/24"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_empty():
    with pytest.raises(ipaddress.AddressValueError):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_netmask():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.5.0/224"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/224"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_netmask_empty():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.5.0/"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_no_netmask():
    with pytest.raises(ValueError, match="No prefix for subnet: 10.0.1.0"):
        subnets = {
            "net1": "10.0.1.0",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_hostbits():
    with pytest.raises(ValueError, match="10.0.2.0/14 has host bits set"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/14",
            "net3": "10.0.3.3/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_hostbits2():
    with pytest.raises(ValueError, match="10.0.3.3/24 has host bits set"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.3/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_fail_mixed():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.3.0/"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/",
            "net4": "10.0.4.0/224",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_valid_subnets_multiple():
    subnets1 = {
        "net1": "10.0.1.0/24",
        "net2": "10.0.2.0/24",
        "net3": "10.0.3.0/24",
        "net4": "10.0.4.0/24",
        "net5": "10.0.5.0/24"
    }

    subnets2 = {
        "net1": "10.1.1.0/24",
        "net2": "10.1.2.0/24",
        "net3": "10.1.3.0/24",
        "net4": "10.1.4.0/24",
        "net5": "10.1.5.0/24"
    }

    net_validator.validate_subnets(subnets1, subnets2)


def test_valid_subnets_multiple_fail_first():
    with pytest.raises(ValueError, match="10.0.3.3/24 has host bits set"):
        subnets1 = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.3/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        subnets2 = {
            "net1": "10.1.1.0/24",
            "net2": "10.1.2.0/24",
            "net3": "10.1.3.0/24",
            "net4": "10.1.4.0/24",
            "net5": "10.1.5.0/24"
        }

        net_validator.validate_subnets(subnets1, subnets2)


def test_valid_subnets_multiple_fail_second():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.3.0/"):
        subnets1 = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        subnets2 = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/",
            "net4": "10.0.4.0/224",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets1, subnets2)


# #############################################################################
# ########################## INTERFACES #######################################
# #############################################################################
def test_valid_ifaces_success():
    interfaces = {
        "topo-r01": {
            "eth0": "10.0.1.3/24",
            "eth1": "10.0.2.3/24",
            "eth2": "10.0.3.2/24",
        },
        "topo-r02": {
            "eth5": "10.0.2.2/24",
            "eth4": "10.0.5.1/24",
        },
        "topo-r03": {
            "eth2": "10.0.1.4/24",
            "eth6": "10.0.2.4/24",
            "eth3": "10.0.4.2/24",
            "eth0": "10.0.5.5/24"
        }
    }

    net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_invalid():
    with pytest.raises(ipaddress.AddressValueError):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/24",
            },
            "topo-r02": {
                "eth5": "10.0.2.2/24",
                "eth4": "10.0.514.1/24",
            },
            "topo-r03": {
                "eth2": "10.0.1.4/24",
                "eth6": "10.0.2.4/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_empty():
    with pytest.raises(ipaddress.AddressValueError):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/24",
            },
            "topo-r02": {
                "eth5": "10.0.2.2/24",
                "eth4": "10.0.5.1/24",
            },
            "topo-r03": {
                "eth2": "",
                "eth6": "10.0.2.4/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_netmask():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.5.1/224"):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/24",
            },
            "topo-r02": {
                "eth5": "10.0.2.2/24",
                "eth4": "10.0.5.1/224",
            },
            "topo-r03": {
                "eth2": "10.0.1.4/24",
                "eth6": "10.0.2.4/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_netmask_empty():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.3.2/"):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/",
            },
            "topo-r02": {
                "eth5": "10.0.2.2/24",
                "eth4": "10.0.5.1/224",
            },
            "topo-r03": {
                "eth2": "10.0.1.4/24",
                "eth6": "10.0.2.4/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_no_netmask():
    with pytest.raises(ValueError, match="No prefix for subnet: 10.0.2.2"):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/14",
            },
            "topo-r02": {
                "eth5": "10.0.2.2",
                "eth4": "10.0.5.1/24",
            },
            "topo-r03": {
                "eth2": "10.0.1.4/24",
                "eth6": "10.0.2.422/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)


def test_valid_ifaces_fail_mixed():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.3.2/"):
        interfaces = {
            "topo-r01": {
                "eth0": "10.0.1.3/24",
                "eth1": "10.0.2.3/24",
                "eth2": "10.0.3.2/",
            },
            "topo-r02": {
                "eth5": "10.0.2.2",
                "eth4": "10.0.5.1/24",
            },
            "topo-r03": {
                "eth2": "10.0.1.4/24",
                "eth6": "10.0.2.422/24",
                "eth3": "10.0.4.2/24",
                "eth0": "10.0.5.5/24"
            }
        }

        net_validator.validate_interfaces(interfaces)
