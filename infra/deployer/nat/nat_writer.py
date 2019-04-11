import csv
import constants as const

# TODO adapt to the simpler format
def write_subnets(output_dir: str, subnets: dict):
    subnets_file = "{}/{}".format(output_dir, const.SUBNETS_FILE)

    with open(subnets_file, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for s in subnets.values():
            writer.writerow([s["subnet"], s["sim_subnet"]])


def write_ifaces(output_dir: str, ifaces: dict):
    ifaces_file = "{}/{}".format(output_dir, const.IFACES_FILE)
    write_file(ifaces_file, ifaces)


def write_ips(output_dir: str, ips: dict):
    ips_file = "{}/{}".format(output_dir, const.IPS_FILE)
    write_file(ips_file, ips)

# TODO turn to write device configs
def write_file(output_file: str, matched_configs: dict):
    with open(output_file, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

        for dev, matches in matched_configs.items():
            for orig_config, sim_config in matches.items():
                writer.writerow([dev, orig_config, sim_config])
