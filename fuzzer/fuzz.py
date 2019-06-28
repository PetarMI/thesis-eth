from argparse import ArgumentParser
from fuzzer.Fuzzer import Fuzzer


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--depth", dest="depth", required=False,
                        help="The max depth we are checking for failed links")
    parser.add_argument("-a", "--algo", dest="algo", required=False,
                        help="Search algorithm to use")
    args = parser.parse_args()

    fuzzer = Fuzzer()
    fuzzer.prepare_fuzzing(3)
    fuzzer.print_search_strategy()
    fuzzer.verify_deployment()
    fuzzer.fuzz()


main()
