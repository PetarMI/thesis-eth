import ipaddress
import file_reader as fr


def validate_subnets(subnets: dict):
    for subnet in subnets.values():
        validate_subnet(subnet)


def validate_subnet(subnet: str):
    try:
        parsed_subnet = ipaddress.IPv4Network(subnet, strict=True)
        if (parsed_subnet.prefixlen == 32):
            raise ValueError("No prefix for subnet: {}".format(subnet))
    except ipaddress.AddressValueError:
        raise
    except ipaddress.NetmaskValueError as err:
        err.args = ("Invalid netmask: {}".format(subnet),)
        raise
    except ValueError:
        raise


# some_nets = fr.read_sim_subnets("toy")
# validate_subnets(some_nets)
