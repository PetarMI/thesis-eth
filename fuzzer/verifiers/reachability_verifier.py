import pingparsing
from fuzzer.common import file_reader as fr


def verify_ping_reachability(properties: list) -> dict:
    results = dict()

    for idx, prop in enumerate(properties):
        ping_msg = fr.read_ping_file(idx)
        res: dict = check_ping(ping_msg, prop["dest_sim_ip"])

        results.update({idx: res})

    return results


def check_ping(ping_msg: str, dest_sim_ip) -> dict:
    parser = pingparsing.PingParsing()
    stats = parser.parse(ping_msg)

    if stats is None:
        res_status = 3
        res_text = "pingparsing couldn't parse ping results"

        return {
            "status": res_status,
            "text": res_text
        }

    ping_stats = stats.as_dict()

    if ping_stats["destination"] != dest_sim_ip:
        raise ValueError("Error in reachability verifier: ping out of order {}, expected {}".format(
            ping_stats["destination"], dest_sim_ip))

    if ping_stats["packet_transmit"] == ping_stats["packet_receive"]:
        res_status = 0
        res_text = "All packets received"
    elif ping_stats["packet_transmit"] == ping_stats["packet_loss_count"]:
        res_status = 1
        res_text = "All packets lost"
    elif 0 < ping_stats["packet_receive"] < ping_stats["packet_transmit"]:
        res_status = 2
        res_text = "Some packets lost"
    else:
        res_status = 3
        res_text = "Unknown fuckup, check file"

    return {
        "status": res_status,
        "desc": res_text
    }
