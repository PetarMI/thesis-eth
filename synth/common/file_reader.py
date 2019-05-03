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


def validate_link_endpoints(endpoints: list):
    if len(endpoints) != 2:
        raise ValueError("Malformed links file at line {}".format_map(idx + 1))
