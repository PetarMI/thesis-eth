from synth.common import constants_synth as const
from synth.common import file_writer as fw


def generate_config_files(cisco_configs, topo_name):
    frr_configs = dict()

    for hostname, host_configs in cisco_configs.items():
        host_configs = []

        host_configs.extend(generate_meta(hostname))
        host_configs.extend(generate_file_end())

        frr_configs.update({hostname: host_configs})

    fw.write_config_files(topo_name, frr_configs)


def generate_meta(hostname):
    meta = [const.CMD_FRR_VER, const.CMD_FRR_DEF, const.CMD_HOST.format(hostname),
            const.CMD_INTEGRATED, const.CMD_END_SEC]

    return meta


def generate_file_end():
    return ["line vty", "!"]
