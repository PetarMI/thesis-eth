#import pingparsing
from fuzzer.common import file_reader as fr


def main():
    properties: list = fr.read_reachability_properties()
    print(properties)


if __name__ == '__main__':
    main()
