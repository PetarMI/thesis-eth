import pytest
from synth.cisco import links_parser as lp


def test_get_sim_net_empty_track():
    host = "London"
    endpoint = "Amsterdam"
    links = dict()

    res_sim_net = lp.get_sim_net(host, endpoint, links)
    expected_sim_net = "net-london-amsterdam"

    assert(res_sim_net == expected_sim_net)


def test_get_sim_net_success_no_endpoint():
    host = "London"
    endpoint = "Amsterdam"
    created_links = {
        "London": {
            "Paris": "net-paris-london",
            "Brussels": "net-brussels-london",
            "Lisbon": "net-london-lisbon"
        },
        "Lisbon": {
            "London": "net-london-lisbon"
        }
    }

    res_sim_net = lp.get_sim_net(host, endpoint, created_links)
    expected_sim_net = "net-london-amsterdam"

    assert(res_sim_net == expected_sim_net)


def test_get_sim_net_success_match():
    host = "London"
    endpoint = "Amsterdam"
    created_links = {
        "London": {
            "Paris": "net-paris-london",
            "Brussels": "net-brussels-london",
            "Lisbon": "net-london-lisbon"
        },
        "Lisbon": {
            "London": "net-london-lisbon"
        },
        "Amsterdam": {
            "Brussels": "net-brussels-amsterdam",
            "Rotterdam": "net-rotterdam-amsterdam",
            "Frankfurt": "net-frankfurt-amsterdam",
            "London": "net-amsterdam-london"
        }
    }

    res_sim_net = lp.get_sim_net(host, endpoint, created_links)
    expected_sim_net = "net-amsterdam-london"

    assert(res_sim_net == expected_sim_net)


def test_validate_links_success():
    raw_links = {
        "Lyon": [
            "Paris",
            "Kiev"
        ],
        "Kiev": [
            "Paris",
            "Lyon"
        ],
        "Paris": [
            "Kiev",
            "Lyon",
        ]
    }

    lp.validate_links(raw_links)


def test_validate_links_fail_no_entry():
    with pytest.raises(ValueError, match="Missing top-level entry for host Vratsa"):
        raw_links = {
            "Lyon": [
                "Paris",
                "Kiev"
            ],
            "Kiev": [
                "Paris",
                "Lyon",
                "Vratsa"
            ],
            "Paris": [
                "Lyon",
                "Kiev"
            ]
        }

        lp.validate_links(raw_links)


def test_validate_links_fail_no_duplex1():
    with pytest.raises(ValueError, match="No duplex link between Lyon and Kiev"):
        raw_links = {
            "Lyon": [
                "Paris",
                "Kiev"
            ],
            "Kiev": [
                "Paris"
            ],
            "Paris": [
                "Lyon",
                "Kiev"
            ]
        }

        lp.validate_links(raw_links)


def test_validate_links_fail_no_duplex2():
    with pytest.raises(ValueError, match="No duplex link between Paris and Kiev"):
        raw_links = {
            "Lyon": [
                "Paris",
                "Kiev"
            ],
            "Kiev": [
                "Lyon"
            ],
            "Paris": [
                "Lyon",
                "Kiev"
            ]
        }

        lp.validate_links(raw_links)
