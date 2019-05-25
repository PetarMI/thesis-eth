import pytest
from FuzzData import parse_net2devices


def test_net2dev_exact():
    containers: list = [
        {
            "name": "r01",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet12"},
                           {"network": "wnet13"},
                           {"network": "wnet14"}]
        },
        {
            "name": "r02",
            "interfaces": [{"network": "wnet20"},
                           {"network": "wnet12"},
                           {"network": "wnet23"},
                           {"network": "wnet24"}]
        },
        {
            "name": "r03",
            "interfaces": [{"network": "wnet30"},
                           {"network": "wnet13"},
                           {"network": "wnet23"},
                           {"network": "wnet34"}]
        },
        {
            "name": "r04",
            "interfaces": [{"network": "wnet40"},
                           {"network": "wnet14"},
                           {"network": "wnet24"},
                           {"network": "wnet34"}]
        }
    ]

    res_net2dev = parse_net2devices("topo", containers)
    expected_net2dev = {
        "topo-wnet10": ["topo-r01"],
        "topo-wnet20": ["topo-r02"],
        "topo-wnet30": ["topo-r03"],
        "topo-wnet40": ["topo-r04"],
        "topo-wnet12": ["topo-r01", "topo-r02"],
        "topo-wnet13": ["topo-r01", "topo-r03"],
        "topo-wnet14": ["topo-r01", "topo-r04"],
        "topo-wnet23": ["topo-r02", "topo-r03"],
        "topo-wnet24": ["topo-r02", "topo-r04"],
        "topo-wnet34": ["topo-r03", "topo-r04"],
    }

    assert (res_net2dev == expected_net2dev)


def test_net2dev_part():
    containers: list = [
        {
            "name": "r01",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet20"}]
        },
        {
            "name": "r02",
            "interfaces": [{"network": "wnet10"},
                           {"network": "wnet11"},
                           {"network": "wnet12"}]
        },
        {
            "name": "r03",
            "interfaces": [{"network": "wnet20"},
                           {"network": "wnet21"},
                           {"network": "wnet22"}]
        }
    ]

    res_net2dev = parse_net2devices("topo", containers)
    expected_net2dev = {
        "topo-wnet10": ["topo-r01", "topo-r02"],
        "topo-wnet20": ["topo-r01", "topo-r03"],
        "topo-wnet11": ["topo-r02"],
        "topo-wnet12": ["topo-r02"],
        "topo-wnet21": ["topo-r03"],
        "topo-wnet22": ["topo-r03"]
    }

    assert(res_net2dev == expected_net2dev)


def test_net2dev_empty():
    containers: list = []

    res_net2dev = parse_net2devices("topo", containers)
    expected_net2dev = {}

    assert(res_net2dev == expected_net2dev)


def test_net2dev_many_conns():
    with pytest.raises(ValueError, match="More than two containers connected to network topo-wnet10"):
        containers: list = [
            {
                "name": "r01",
                "interfaces": [{"network": "wnet10"},
                               {"network": "wnet20"}]
            },
            {
                "name": "r02",
                "interfaces": [{"network": "wnet10"},
                               {"network": "wnet11"},
                               {"network": "wnet12"}]
            },
            {
                "name": "r03",
                "interfaces": [{"network": "wnet20"},
                               {"network": "wnet21"},
                               {"network": "wnet22"},
                               {"network": "wnet10"}]
            }
        ]

        parse_net2devices("topo", containers)
