import csv
from argparse import ArgumentParser
import topo_parser as tp


def main(topology_file: str):
    topo: dict = tp.import_topo(topology_file)
    topo_meta: dict = tp.find_metadata(topo)
    containers: list = tp.find_containers(topo)

    container_data: list = extract_data(topo_meta, containers)
    write_csv(container_data)


def extract_data(topo_meta: dict, containers: list) -> list:
    topo_name: str = topo_meta.get("name")
    container_data = []

    for c in containers:
        container_name = topo_name + "-" + c.get("name")
        data = [container_name, c.get("type")]
        container_data.append(data)

    return container_data


def write_csv(container_data: list):
    with open('person.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(container_data)

    csvFile.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename",
                        help="Topology file")
    args = parser.parse_args()

    topo_name: str = args.filename

    main(topo_name)
