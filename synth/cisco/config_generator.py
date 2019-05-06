from synth.common import constants_synth as const
from synth.common import file_writer as fw


def generate_config_files(cisco_configs, topo_name):
    frr_configs = dict()

    for hostname, host_configs in cisco_configs.items():
        host_instr = []

        host_instr.extend(generate_meta(hostname))
        host_instr.extend(generate_interfaces(host_configs["interfaces"]))
        host_instr.extend(generate_router_section())
        host_instr.extend(generate_file_end())

        frr_configs.update({hostname: host_instr})

    fw.write_config_files(topo_name, frr_configs)


def generate_interfaces(host_interfaces: list) -> list:
    all_ifaces = []

    for interface in host_interfaces:
        all_ifaces.extend(generate_interface_instr(interface))

    return all_ifaces


def generate_interface_instr(interface: dict) -> list:
    instr = []

    instr.append("interface {}".format(interface["name"]))
    instr.append(const.CMD_END_SEC)

    return instr


def generate_router_section() -> list:
    # TODO
    return []


def generate_meta(hostname) -> list:
    meta = [const.CMD_FRR_VER, const.CMD_FRR_DEF, const.CMD_HOST.format(hostname),
            const.CMD_INTEGRATED, const.CMD_END_SEC]

    return meta


def generate_file_end() -> list:
    return ["line vty", "!"]
