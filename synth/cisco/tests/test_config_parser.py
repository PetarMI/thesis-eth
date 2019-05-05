import pytest
import ciscoconfparse
from synth.cisco import config_parser as cp


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
