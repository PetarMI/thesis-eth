import ipaddress
import pytest
import net_validator


def test_subnets_success():
    subnets = {
        "net1": "10.0.1.0/24",
        "net2": "10.0.2.0/24",
        "net3": "10.0.3.0/24",
        "net4": "10.0.4.0/24",
        "net5": "10.0.5.0/24"
    }

    net_validator.validate_subnets(subnets)


def test_subnets_fail_invalid():
    with pytest.raises(ipaddress.AddressValueError):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.413.0/24",
            "net5": "10.0.5.0/24"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_empty():
    with pytest.raises(ipaddress.AddressValueError):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/24"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_netmask():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.5.0/224"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/224"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_netmask_empty():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.5.0/"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0/"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_no_netmask():
    with pytest.raises(ValueError, match="No prefix for subnet: 10.0.1.0"):
        subnets = {
            "net1": "10.0.1.0",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_hostbits():
    with pytest.raises(ValueError, match="10.0.2.0/14 has host bits set"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/14",
            "net3": "10.0.3.3/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_hostbits2():
    with pytest.raises(ValueError, match="10.0.3.3/24 has host bits set"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.3/24",
            "net4": "10.0.4.0/24",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)


def test_subnets_fail_mixed():
    with pytest.raises(ipaddress.NetmaskValueError, match="Invalid netmask: 10.0.3.0/"):
        subnets = {
            "net1": "10.0.1.0/24",
            "net2": "10.0.2.0/24",
            "net3": "10.0.3.0/",
            "net4": "10.0.4.0/224",
            "net5": "10.0.5.0"
        }

        net_validator.validate_subnets(subnets)
