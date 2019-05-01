import pingparsing
from fuzzer.common import file_reader as fr


def main():
    properties: list = fr.read_reachability_properties()
    verify_reachability(properties)


def verify_reachability(properties: list):
    for idx, prop in enumerate(properties):
        ping_msg = fr.read_ping_file(idx)
        success, ver_res = check_ping(ping_msg, prop["dest_sim_ip"])

        print("Reachability Property {}:".format(idx))

        if success:
            print("Success: {}".format(ver_res))
        else:
            print("Failed: {}".format(ver_res))


def check_ping(ping_msg: str, dest_sim_ip) -> (bool, str):
    parser = pingparsing.PingParsing()
    stats = parser.parse(ping_msg)

    if stats is None:
        return False, "ERROR: pinparsing couldn't parse ping results"

    ping_stats = stats.as_dict()

    if ping_stats["destination"] != dest_sim_ip:
        raise ValueError("Error in reachability verifier: ping out of order {}, expected {}".format(
            ping_stats["destination"], dest_sim_ip))

    if ping_stats["packet_transmit"] == ping_stats["packet_receive"]:
        return True, "INFO: All packets received"
    elif ping_stats["packet_transmit"] == ping_stats["packet_loss_count"]:
        return False, "ERROR: All packets lost"
    elif 0 < ping_stats["packet_receive"] < ping_stats["packet_transmit"]:
        return True, "WARNING: Some packets lost"
    else:
        return False, "ERROR: Fuckup, check file"


if __name__ == '__main__':
    main()
