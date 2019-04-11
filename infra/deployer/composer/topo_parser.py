import json


container_types = {
    "frr": "phynet:latest"
}


def import_topo(topo_file: str) -> dict:
    """ Function to load the topology encoded in json format """
    # topo_file: str = const.TOPO_DIR + topo_name + const.TOPO_EXTENSION

    with open(topo_file) as json_data:
        topo = json.load(json_data)

    return topo


def find_metadata(topo: dict) -> dict:
    return check_none(topo.get("meta", None))


def find_nets(topo: dict) -> list:
    return check_none(topo.get("networks", None))


def find_containers(topo: dict) -> list:
    return check_none(topo.get("containers", None))


def find_topo_name(topo: dict) -> str:
    return check_none(find_metadata(topo).get("name", None))


def find_container_nets(container: dict) -> list:
    interfaces = safe_get(container, "interfaces")
    container_nets = []

    for i in interfaces:
        container_nets.append(safe_get(i, "network"))

    return container_nets


def get_container_image(container_type: str) -> str:
    container_image = container_types.get(container_type)

    if container_image is None:
        raise KeyError("Unsupported container type")

    return container_image


def safe_get(some_dict: dict, key: str):
    return check_none(some_dict.get(key, None))


def check_none(val):
    if val is None:
        raise KeyError("Missing key")

    return val
