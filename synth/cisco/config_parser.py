import ciscoconfparse
from ciscoconfparse.ccp_util import IPv4Obj
import ipaddress


def parse_configs(cisco_configs: dict) -> dict:
    """ Main function for parsing cisco configs """
    parsed_configs = dict()

    for hostname, cisco_config in cisco_configs.items():
        try:
            parsed_config: dict = parse_host(cisco_config)
            parsed_configs.update({hostname: parsed_config})
            print(parsed_configs)
        except Exception as exc:
            raise ValueError("Error in {} configs".format(hostname)) from exc
        break
    return parsed_configs


def parse_host(host_cisco_config: str) -> dict:
    confparser = ciscoconfparse.CiscoConfParse(host_cisco_config.splitlines())

    parsed_configs = dict()
    parsed_configs["interfaces"] = parse_interfaces(confparser)
    # TODO: this just checks whether a router ospf section is present
    router: dict = parse_router(confparser)

    return parsed_configs


def parse_interfaces(confparser) -> list:
    """ Main function for parsing interfaces """
    interfaces = []
    interface_cmds = confparser.find_objects(r"^interface ")

    for interface_cmd in interface_cmds:
        interface = dict()

        interface["name"] = interface_cmd.text[len("interface "):]
        interface["ip"] = extract_ip_address(interface_cmd)
        interface["cost"] = extract_cost(interface_cmd)
        interface["area"] = extract_iface_area(interface_cmd)
        interface["description"] = extract_description(interface_cmd)

        interfaces.append(interface)

    return interfaces


def parse_router(confparser) -> dict:
    """ Main function for parsing the router section """
    router = dict()
    router_cmd = confparser.find_objects(r"^router ospf ")
    validate_cisco_commands(router_cmd, "router", strict=True)

    return router


def extract_ip_address(interface_cmd) -> str:
    IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"
    ip_addr_instr = interface_cmd.re_search_children(IPv4_REGEX)
    validate_cisco_commands(ip_addr_instr, "ip address", strict=True)

    ipv4_addr_obj = interface_cmd.re_match_iter_typed(IPv4_REGEX, result_type=IPv4Obj)
    ip_iface = "{}/{}".format(ipv4_addr_obj.ip.exploded,
                              ipv4_addr_obj.netmask.exploded)
    # ensure correct IPv4Interface format
    ipv4_interface = ipaddress.IPv4Interface(ip_iface)

    return str(ipv4_interface)


# @Tested
def extract_cost(interface_cmd) -> str:
    cost_commands = interface_cmd.re_search_children(r"^ ip ospf cost ")
    validate_cisco_commands(cost_commands, "ospf cost")
    cost = None

    for cmd in cost_commands:
        cost = str(int(cmd.text.strip()[len("ip ospf cost "):]))

    return cost


# @Tested
def extract_iface_area(interface_cmd) -> str:
    area_commands = interface_cmd.re_search_children(r"^ ip ospf [0-9]* area ")
    validate_cisco_commands(area_commands, "area")
    area = None

    for cmd in area_commands:
        area = str(int(cmd.text.split()[-1]))

    return area


# @Tested
def extract_description(interface_cmd) -> str:
    descr_commands = interface_cmd.re_search_children(r"^ description ")
    validate_cisco_commands(descr_commands, "description")
    description = None

    for cmd in descr_commands:
        description = cmd.text.strip()[len("description "):].strip('\"')

    return description


# @Tested
def validate_cisco_commands(commands, cmd_type: str, **kwargs):
    strict = kwargs.get("strict", False)

    if strict and len(commands) == 0:
        raise ValueError("No {} command at interface".format(cmd_type))

    if len(commands) > 1:
        raise ValueError("More than one {} command at interface".format(cmd_type))


# def validate_cisco_interfaces(interface_cmds):
#     IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"
#
#     for interface_cmd in interface_cmds:
#         description_cmds = interface_cmd.re_search_children(r"^ description ")
#         ip_addr_instr = interface_cmd.re_search_children(IPv4_REGEX)
#         cost_cmds = interface_cmd.re_search_children(r"^ ip ospf cost ")
#
#         if len(description_cmds) > 1:
#             raise ValueError("More than one description command found")
#
#         if len(ip_addr_instr) == 0:
#             raise ValueError("No ip address command at interface")
#
#         if len(ip_addr_instr) > 1:
#             raise ValueError("More than one ip address command at interface")
#
#         if len(cost_cmds) > 1:
#             raise ValueError("More than one ospf cost command")
