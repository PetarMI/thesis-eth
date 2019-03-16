def find_nets(topo: dict) -> list:
    return check_none(topo.get("networks", None))


def find_containers(topo: dict, container_type: str) -> list:
    topo_containers = check_none(topo.get("containers", None))

    return topo_containers.get(container_type, None)


def check_none(val):
    if val is None:
        raise KeyError("Missing key")

    return val
