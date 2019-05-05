import pytest
import ciscoconfparse
import ipaddress
from synth.cisco import config_parser as cp
from synth.common import file_reader as fr


######################################################
# ################### High-level ##@##################
######################################################
def test_interface_parsing_success():
    raw_configs = fr.read_host_configs("test_topo", "Costa_Rica")
    confparser = ciscoconfparse.CiscoConfParse(raw_configs.splitlines())

    res_ifaces = cp.parse_host_interfaces(confparser)
    expected_ifaces = [
        {
            "name": "Fa0/0",
            "ip": "100.0.36.1/24",
            "cost": None,
            "area": None,
            "description": "To 100.0.36.0/24"
        },
        {
            "name": "Fa1/1",
            "ip": "10.0.0.141/31",
            "cost": "1",
            "area": "0",
            "description": None
        },
        {
            "name": "Fa0/1",
            "ip": "10.0.0.161/31",
            "area": "0",
            "cost": None,
            "description": "To Nicaragua"
        },
        {
            "name": "Fa1/0",
            "ip": "10.0.0.117/31",
            "cost": "2",
            "area": "0",
            "description": "To NodeID9"
        }
    ]

    assert(res_ifaces == expected_ifaces)


######################################################
# ################## IP extraction ###################
######################################################
def test_extract_ip_success():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf 100 area 0",
        " ip ospf cost 1",
        " description \"To Roma\"",
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_ip = cp.extract_ip_address(interface_cmds[0])

    expected_ip = "10.0.0.73/31"

    assert (res_ip == expected_ip)


def test_extract_ip_success2():
    configs = [
        "interface Fa1/0",
        " ip address 192.168.10.69 255.255.255.0",
        " ip ospf 100 area 0",
        " ip ospf cost 1",
        " description \"To Roma\"",
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_ip = cp.extract_ip_address(interface_cmds[0])

    expected_ip = "192.168.10.69/24"

    assert (res_ip == expected_ip)


def test_extract_ip_fail_no_ip():
    with pytest.raises(ValueError, match="No ip address command at interface"):
        configs = [
            "interface Fa1/0",
            " ip ospf 100 area 0",
            " ip ospf cost 1",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_ip_address(interface_cmds[0])


def test_extract_ip_fail_many_ips():
    with pytest.raises(ValueError, match="More than one ip address command at interface"):
        configs = [
            "interface Fa1/0",
            " ip address 192.168.10.69 255.255.255.0",
            " ip ospf 100 area 0",
            " ip address 10.0.0.73 255.255.255.254",
            " ip ospf cost 1",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_ip_address(interface_cmds[0])


def test_extract_ip_fail_invalid_ip():
    with pytest.raises(ipaddress.AddressValueError):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.292.4 255.255.255.0",
            " ip ospf 100 area 0",
            " ip ospf cost 1",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_ip_address(interface_cmds[0])


def test_extract_ip_fail_invalid_netmask():
    with pytest.raises(ipaddress.NetmaskValueError):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.22.4 255.10.255.0",
            " ip ospf 100 area 0",
            " ip ospf cost 1",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_ip_address(interface_cmds[0])


######################################################
# ################# Area extraction ##################
######################################################
def test_extract_iface_area_success():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf 100 area 0",
        " ip ospf cost 1",
        " description \"To Roma\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_area = cp.extract_iface_area(interface_cmds[0])

    expected_area = "0"

    assert (res_area == expected_area)


def test_extract_iface_area_success_no_id():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf area 0",
        " ip ospf cost 1",
        " description \"To Roma\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_area = cp.extract_iface_area(interface_cmds[0])

    expected_area = "0"

    assert (res_area == expected_area)


def test_extract_iface_area_success_none():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf cost 1",
        " description \"To Roma\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_area = cp.extract_iface_area(interface_cmds[0])

    expected_area = None

    assert (res_area == expected_area)


def test_extract_iface_area_fail_many():
    with pytest.raises(ValueError, match="More than one area command at interface"):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.0.73 255.255.255.254",
            " ip ospf 100 area 0",
            " ip ospf cost 1",
            " description \"To Roma\"",
            " ip ospf 100 area 1",
            " speed auto",
            " duplex auto"
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_iface_area(interface_cmds[0])


def test_extract_iface_area_fail_not_int():
    with pytest.raises(ValueError):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.0.73 255.255.255.254",
            " ip ospf 100 area 0 doesntbelong",
            " ip ospf cost 1",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_iface_area(interface_cmds[0])


######################################################
# ################# Cost extraction ##################
######################################################
def test_extract_iface_cost_success():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf 100 area 0",
        " ip ospf cost 1",
        " description \"To Roma\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_cost = cp.extract_cost(interface_cmds[0])

    expected_cost = "1"

    assert (res_cost == expected_cost)


def test_extract_iface_cost_success_none():
    configs = [
        "interface Fa1/0",
        " ip address 10.0.0.73 255.255.255.254",
        " ip ospf 100 area 0",
        " description \"To Roma\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_cost = cp.extract_cost(interface_cmds[0])

    expected_cost = None

    assert (res_cost == expected_cost)


def test_extract_iface_cost_fail_many():
    with pytest.raises(ValueError, match="More than one ospf cost command at interface"):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.0.73 255.255.255.254",
            " ip ospf 100 area 0",
            " ip ospf cost 1",
            " description \"To Roma\"",
            " ip ospf cost 2",
            " speed auto",
            " duplex auto"
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_cost(interface_cmds[0])


def test_extract_iface_cost_fail_not_int():
    with pytest.raises(ValueError):
        configs = [
            "interface Fa1/0",
            " ip address 10.0.0.73 255.255.255.254",
            " ip ospf 100 area 0",
            " ip ospf cost 1doesntbelong",
            " description \"To Roma\"",
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_cost(interface_cmds[0])


######################################################
# ############ Description extraction ################
######################################################
def test_extract_description_success():
    configs = [
        "interface Fa0/0",
        " ip address 100.0.27.1 255.255.255.0",
        " ip ospf 100 area 0",
        " description \"To Lesura\"",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_description = cp.extract_description(interface_cmds[0])

    expected_description = "To Lesura"

    assert res_description == expected_description


def test_extract_description_success_none():
    configs = [
        "interface Fa0/0",
        " ip address 100.0.27.1 255.255.255.0",
        " speed auto",
        " duplex auto"
        "!"
    ]

    confparser = ciscoconfparse.CiscoConfParse(configs)
    interface_cmds = confparser.find_objects(r"^interface ")
    res_description = cp.extract_description(interface_cmds[0])

    assert (res_description is None)


def test_extract_description_fail():
    with pytest.raises(ValueError, match="More than one description command at interface"):
        configs = [
            "interface Fa0/0",
            " ip address 100.0.27.1 255.255.255.0",
            " description \"Lesura\"",
            " description \"Vratsa\"",
            " speed auto",
            " duplex auto"
            "!"
        ]

        confparser = ciscoconfparse.CiscoConfParse(configs)
        interface_cmds = confparser.find_objects(r"^interface ")
        cp.extract_description(interface_cmds[0])


######################################################
# ################## Validation  #####################
######################################################
def test_validate_command_success_strict():
    commands = ["some command"]
    cp.validate_cisco_commands(commands, "whatever", strict=True)


def test_validate_command_fail_strict_none():
    with pytest.raises(ValueError, match="No whatever command at interface"):
        commands = []
        cp.validate_cisco_commands(commands, "whatever", strict=True)


def test_validate_command_fail_strict_many():
    with pytest.raises(ValueError, match="More than one whatever command at interface"):
        commands = ["many", "commands"]
        cp.validate_cisco_commands(commands, "whatever", strict=True)
