import json
import random
import ipaddress
from argparse import ArgumentParser
from benchmarks.fuzzer.scripts import constants_fuzz_bench as const


def main():
    parser = ArgumentParser()
    parser.add_argument("-t", "--topo", dest="topology", required=True,
                        help="The topology to generate reachability props for")
    parser.add_argument("-n", "--num", dest="number", required=True,
                        help="The number of properties to generate")
    args = parser.parse_args()

    topo_name: str = args.topology
    num_props = int(args.number)

    properties: list = generate_properties(topo_name, num_props)
    write_properties(properties, topo_name)


def generate_properties(topo_name: str, n: int) -> list:
    topo_data: dict = read_topo_data(topo_name)
    # print(json.dumps(topo_data, indent=4))

    properties = []
    print(list(topo_data))
    for i in range(1, n):
        src_name = random.choice(list(topo_data))
        dest_name = random.choice(list(topo_data))

        while src_name == dest_name:
            dest_name = random.choice(list(topo_data))

        dest_ip = topo_data[dest_name]

        properties.append({
            "src": src_name,
            "dest": dest_ip,
            "dest_name": dest_name
        })

    return properties


def read_topo_data(topo_name: str) -> dict:
    topo_file = "{0}/{1}/{1}.topo".format(const.TOPO_DIR, topo_name)

    with open(topo_file) as json_file:
        topo = json.load(json_file)

    topo_data = dict()

    for container in topo["containers"]:
        found_static_net = False

        for iface in container["interfaces"]:
            if iface["ipaddr"].startswith("100."):
                static_net_ip = str(ipaddress.IPv4Interface(iface["ipaddr"]).ip)
                topo_data.update({container["name"]: static_net_ip})
                found_static_net = True
                break

        if not found_static_net:
            raise ValueError("Container {} has no static net".format(container["name"]))

    return topo_data


def write_properties(properties: list, topo_name: str):
    props_filename = const.PROPERTIES_FILE.format(topo_name)
    pretty_props_filename = const.PRETTY_PROPERTIES_FILE.format(topo_name)

    props_file = "{}/{}".format(const.GEN_DIR, props_filename)
    pretty_props_file = "{}/{}".format(const.GEN_DIR, pretty_props_filename)

    with open(props_file, mode='w+') as json_file:
        props_json = {"reachability": properties}
        json_file.write(json.dumps(props_json, indent=4))

    with open(pretty_props_file, mode='w+') as json_file:
        for idx, prop in enumerate(properties, start=1):
            json_file.write("{}. {} ---> {}\n".format(idx, prop["src"], prop["dest_name"]))


main()
