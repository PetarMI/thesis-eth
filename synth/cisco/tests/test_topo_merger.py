import pytest
import ipaddress
from synth.cisco import topo_merger as tm
from synth.cisco import config_parser as cp
from synth.common import file_reader as fr


###############################################################################
# #################### Multiple host interfaces ###############################
###############################################################################
def test_match_all_ifaces():
    host = "Kiev"
    host_links = {
        "Bucharest": "net-kiev-bucharest",
        "Warsaw": "net-kiev-warsaw"
    }
    host_ifaces = [
            {
                "name": "Fa0/0",
                "ip": "100.0.1.1/24",
                "cost": None,
                "area": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.0.6/31",
                "cost": None,
                "description": "To Bucharest"
            },
            {
                "name": "Fa1/0",
                "ip": "10.0.0.8/31",
                "area": "0",
                "description": "To Warsaw"
            }
        ]

    host_neighbours = {
        "Bucharest": [
            {
                "name": "Fa0/1",
                "ip": "10.0.0.61/31",
                "description": "To Budapest"
            },
            {
                "name": "Fa1/1",
                "ip": "10.0.0.7/31",
                "area": "0",
                "description": "To Kiev"
            }
        ],
        "Warsaw": [
            {
                "name": "Fa0/0",
                "ip": "100.0.32.1/24",
                "area": None,
                "description": "To 100.0.32.0/24"
            },
            {
                "name": "Fa1/0",
                "ip": "10.0.0.9/31",
                "description": "To Kiev"
            }
        ]
    }

    res_ifaces = tm.find_host_nets(host, host_ifaces, host_links, host_neighbours)
    expected_ifaces = [
        {
            "ip": "100.0.1.1/24",
            "net": "net-kiev",
            "subnet": "100.0.1.0/24"
        },
        {
            "ip": "10.0.0.6/31",
            "net": "net-kiev-bucharest",
            "subnet": "10.0.0.6/31"
        },
        {
            "ip": "10.0.0.8/31",
            "net": "net-kiev-warsaw",
            "subnet": "10.0.0.8/31"
        }
    ]

    assert(res_ifaces == expected_ifaces)


###############################################################################
# #################### Multiple neighbour search ##############################
###############################################################################
def test_search_multiple_neighbours():
    host_net = ipaddress.IPv4Network("10.0.56.0/24")
    host_links = {
        "Zurich": "net-zurich-milan",
        "Roma": "net-roma-milan"
    }

    neighbours = {
        "Zurich": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.1/24",
                "area": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.12.96.69/24",
                "cost": "1",
                "area": None,
                "description": "To Budapest"
            }
        ],
        "Roma": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.2/24",
                "cost": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.56.69/24",
                "cost": None,
                "area": "0",
                "description": "To Budapest"
            }
        ]
    }

    res_net = tm.search_neighbours(host_net, neighbours, host_links)
    expected_net = "net-roma-milan"

    assert(res_net == expected_net)


def test_search_multiple_neighbours_weirder():
    host_net = ipaddress.IPv4Network("10.0.56.0/24")
    host_links = {
        "Zurich": "net-zurich-milan",
        "Roma": "net-roma-milan",
        "Vratsa": "net-milan-vratsa"
    }

    neighbours = {
        "Zurich": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.1/24",
                "area": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.12.96.69/24",
                "cost": "1",
                "area": None,
                "description": "To Budapest"
            }
        ],
        "Roma": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.2/24",
                "cost": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.56.69/24",
                "cost": None,
                "area": "0",
                "description": "To Budapest"
            }
        ]
    }

    res_net = tm.search_neighbours(host_net, neighbours, host_links)
    expected_net = "net-roma-milan"

    assert(res_net == expected_net)


def test_search_multiple_neighbours_no_match():
    host_net = ipaddress.IPv4Network("10.0.56.0/31")
    host_links = {
        "Zurich": "net-zurich-milan",
        "Roma": "net-roma-milan"
    }

    neighbours = {
        "Zurich": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.1/24",
                "area": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.12.96.69/24",
                "cost": "1",
                "area": None,
                "description": "To Budapest"
            }
        ],
        "Roma": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.2/24",
                "cost": None
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.56.2/31",
                "cost": None,
                "area": "0",
                "description": "To Budapest"
            }
        ]
    }

    res_net = tm.search_neighbours(host_net, neighbours, host_links)
    expected_net = ""

    assert (res_net == expected_net)


def test_search_multiple_neighbours_sanity():
    with pytest.raises(ValueError, match="Sanity check: Network match found in neighbours but "
                                         "host has no link to that neighbour"):
        host_net = ipaddress.IPv4Network("10.0.56.0/31")
        host_links = {
            "Zurich": "net-zurich-milan"
        }

        neighbours = {
            "Zurich": [
                {
                    "name": "Fa0/0",
                    "ip": "100.0.13.1/24",
                    "area": None
                }
            ],
            "Roma": [
                {
                    "name": "Fa0/1",
                    "ip": "10.0.56.1/31",
                    "cost": None,
                    "area": "0",
                    "description": "To Budapest"
                }
            ]
        }

        tm.search_neighbours(host_net, neighbours, host_links)


###############################################################################
# ##################### Single neighbour matching #############################
###############################################################################
def test_search_neighbour_ifaces_match():
    host_net = ipaddress.IPv4Network("10.0.56.0/24")
    neighbour_ifaces = [
        {
            "name": "Fa0/0",
            "ip": "100.0.13.1/24",
            "cost": None,
            "area": None,
            "description": "To 100.0.13.0/24"
        },
        {
            "name": "Fa0/1",
            "ip": "10.0.56.69/24",
            "cost": "1",
            "area": "0",
            "description": "To Budapest"
        }
    ]

    res_match = tm.search_neighbour_ifaces(host_net, neighbour_ifaces)

    assert res_match


def test_search_neighbour_ifaces_match_strange():
    host_net = ipaddress.IPv4Network("10.0.56.18/31", strict=True)
    neighbour_ifaces = [
        {
            "name": "Fa0/0",
            "ip": "100.0.13.1/24",
            "cost": None,
            "area": None,
            "description": "To 100.0.13.0/24"
        },
        {
            "name": "Fa0/1",
            "ip": "10.0.56.19/31",
            "cost": "1",
            "area": "0",
            "description": "To Budapest"
        }
    ]

    res_match = tm.search_neighbour_ifaces(host_net, neighbour_ifaces)

    assert res_match


def test_search_neighbour_ifaces_no_match():
    host_net = ipaddress.IPv4Network("10.0.56.18/31", strict=True)
    neighbour_ifaces = [
        {
            "name": "Fa0/0",
            "ip": "100.0.13.1/24",
            "cost": None,
            "area": None,
            "description": "To 100.0.13.0/24"
        },
        {
            "name": "Fa0/1",
            "ip": "10.0.56.20/31",
            "cost": "1",
            "area": "0",
            "description": "To Budapest"
        }
    ]

    res_match = tm.search_neighbour_ifaces(host_net, neighbour_ifaces)

    assert not res_match


###############################################################################
# ########################## Neighbour picking ################################
###############################################################################
def test_get_neighbour_ifaces_success():
    hosts = ["Bratislava", "Vienna", "Dublin", "Milan", "London", "Roma"]
    host_neighbours = ["Bratislava", "Dublin"]
    test_configs: dict = fr.read_cisco_configs("bics", hosts)

    assert(len(test_configs) == 6)

    configs = cp.parse_configs(test_configs)

    neighbours = tm.get_neighbours_ifaces(host_neighbours, configs)
    expected_neighbours = {
        "Bratislava": [
            {
                "name": "Fa0/0",
                "ip": "100.0.13.1/24",
                "cost": None,
                "area": None,
                "description": "To 100.0.13.0/24"
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.0.36/31",
                "cost": "1",
                "area": "0",
                "description": "To Budapest"
            },
            {
                "name": "Fa1/0",
                "ip": "10.0.0.38/31",
                "cost": "1",
                "area": "0",
                "description": "To Praha"
            },
            {
                "name": "Fa1/1",
                "ip": "10.0.0.40/31",
                "cost": "1",
                "area": "0",
                "description": "To Vienna"
            }

        ],
        "Dublin": [
            {
                "name": "Fa0/0",
                "ip": "100.0.17.1/24",
                "cost": None,
                "area": None,
                "description": "To 100.0.17.0/24"
            },
            {
                "name": "Fa0/1",
                "ip": "10.0.0.66/31",
                "cost": "1",
                "area": "0",
                "description": "To London"
            }

        ]
    }

    assert(neighbours == expected_neighbours)
