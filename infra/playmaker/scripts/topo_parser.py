import json


container_types = {
    "frr": "phynet:1.0"
}


def import_topo(topo_name: str) -> dict:
    """ Function to load the topology encoded in json format """
    # topo_file: str = const.TOPO_DIR + topo_name + const.TOPO_EXTENSION

    with open(topo_name) as json_data:
        topo = json.load(json_data)

    return topo


def find_nets(topo: dict) -> list:
    return check_none(topo.get("networks", None))


def find_containers(topo: dict) -> list:
    return check_none(topo.get("containers", None))


def find_metadata(topo: dict) -> dict:
    return check_none(topo.get("meta", None))


def get_container_image(container_type: str) -> str:
    container_image = container_types.get(container_type)

    if container_image is None:
        raise KeyError("Unsupported container type")

    return container_image


def check_none(val):
    if val is None:
        raise KeyError("Missing key")

    return val
