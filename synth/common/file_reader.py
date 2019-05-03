from synth.common import constants_synth as const


def read_raw_links(topo_name: str) -> dict:
    links_file = "{}/{}/{}".format(const.CISCO_DIR, topo_name, const.LINKS_FILE)
    links = dict()

    with open(links_file) as txt_file:
        for idx, link in enumerate(txt_file):
            endpoints = link.replace('\n', '').split("-")
            validate_link_endpoints(endpoints)

            links.setdefault(endpoints[0], []).append(endpoints[1])

    return links


def read_cisco_configs(topo_name: str, hosts: list) -> dict:
    configs = dict()

    for host in hosts:
        host_config = read_host_configs(topo_name, host)
        configs.update({host: host_config})

    return configs


def read_host_configs(topo_name: str, host: str) -> str:
    config_dir = const.CONFIG_DIR.format(topo_name)
    host_cfg_file = "{}/{}/{}.cfg".format(const.CISCO_DIR, config_dir, host)

    with open(host_cfg_file) as cfg_file:
        configs = cfg_file.read()

    return configs


def validate_link_endpoints(endpoints: list):
    if len(endpoints) != 2:
        raise ValueError("Malformed links file at line {}".format_map(idx + 1))
