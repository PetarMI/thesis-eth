import json
from argparse import ArgumentParser
import os
import csv
import constants_synth as const


def gen_topo_file(num_routers: int):
    topo_dict = {}

    networks: list = gen_networks(num_routers)

    meta_data: dict = gen_meta(num_routers)
    network_data: dict = gen_topo_nets(networks)
    container_data: dict = gen_topo_containers(num_routers, networks)

    topo_dict.update(meta_data)
    topo_dict.update(network_data)
    topo_dict.update(container_data)

    config_data: dict = parse_config_data(meta_data, container_data, networks)

    write_topo_file(topo_dict)
    write_config_data(meta_data, config_data)


def gen_meta(num_routers: int) -> dict:
    meta_dict = {}

    meta_dict.update({
        "meta": {
            "name": "seq",
            "numRouters": num_routers,
            "version": "not really needed"
        }
    })

    return meta_dict


def gen_topo_containers(num_routers: int, networks: list) -> dict:
    containers = []
    vms = gen_vms(num_routers)

    for idx, vm in enumerate(vms):
        container = {
            "name": "r{}".format(idx+1),
            "type": "frr",
            "vm": vm,
            "interfaces": get_cont_ifaces(idx, networks)
        }

        containers.append(container)

    return {"containers": containers}


def gen_topo_nets(networks: list) -> dict:
    topo_nets = []

    for net in networks:
        topo_nets.append({
            "name": net["name"],
            "subnet": net["subnet"]
        })

    return {"networks": topo_nets}


def gen_networks(num_routers: int) -> list:
    num_nets = num_routers + 1
    networks = []

    for i in range(1, num_nets + 1):
        net = {
            "name": "wnet{}".format(i),
            "subnet": "20.10.{}.0/24".format(i),
            "ip1": "20.10.{}.1/24".format(i),
            "ip2": "20.10.{}.2/24".format(i)
        }

        networks.append(net)

    return networks


def gen_vms(num_routers: int) -> list:
    vms = []
    total_vms = 10
    leftover = num_routers % total_vms

    for i in range(1, total_vms + 1):
        current_vm = num_routers//total_vms
        if leftover:
            current_vm += 1
            leftover -= 1

        vms.extend([str(i)] * current_vm)

    return vms


def get_cont_ifaces(idx, networks) -> list:
    ifaces = []

    for i in range(0, 2):
        ifaces.append({
            "network": networks[idx + i]["name"],
        })

    return ifaces


def parse_config_data(meta, containers, networks) -> list:
    topo_name = meta["meta"]["name"]
    config_data = []

    for idx, container in enumerate(containers["containers"]):
        c_name = "{}-{}".format(topo_name, container["name"])
        config_data.append({
            "filename": "{}.conf".format(c_name),
            "hostname": c_name,
            "routerid": get_router_id(idx + 1),
            "subnet1": networks[idx]["subnet"],
            "subnet2": networks[idx + 1]["subnet"],
            "ip1": networks[idx]["ip2"],
            "ip2": networks[idx + 1]["ip1"]
        })

    return config_data


def get_router_id(idx: int):
    return "{0}.{0}.{0}.{0}".format(idx)


def write_topo_file(topo_dict: dict):
    topo_name = topo_dict["meta"]["name"]
    out_dir = "{}/{}".format(const.GEN_DIR, topo_name)
    os.makedirs(out_dir, exist_ok=True)

    out_file = "{}/{}.topo".format(out_dir, topo_name)

    with open(out_file, "w") as topo_file:
        json.dump(topo_dict, topo_file, indent=4)


def write_config_data(meta_data, configs: dict):
    output_file = "{}/{}/configs.csv".format(const.GEN_DIR, meta_data["meta"]["name"])

    with open(output_file, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for config in configs:
            writer.writerow([config["filename"], config["hostname"], config["routerid"],
                             config["subnet1"], config["ip1"],
                             config["subnet2"], config["ip2"]])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-n", "--routers", dest="routers",
                        help="Number of routers to be part of the topology")
    args = parser.parse_args()

    num_devices = int(args.routers)
    if num_devices < 10:
        raise ValueError("At least 10 devices needed")

    gen_topo_file(num_devices)
