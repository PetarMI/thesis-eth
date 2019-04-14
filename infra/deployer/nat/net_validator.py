import ipaddress


# @Tested
def validate_subnets(*args):
    for subnets in args:
        for subnet in subnets.values():
            validate_subnet(subnet)


# @Tested above
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


def validate_interfaces(*args):
    for interfaces in args:
        for config in interfaces.values():
            for ip in config.values():
                validate_interface(ip)


def validate_interface(interface: str):
    try:
        parsed_ip = ipaddress.IPv4Interface(interface)
        if (parsed_ip.network.prefixlen == 32):
            raise ValueError("No prefix for subnet: {}".format(interface))
    except ipaddress.AddressValueError:
        raise
    except ipaddress.NetmaskValueError as err:
        err.args = ("Invalid netmask: {}".format(interface),)
        raise
