#import pingparsing
from fuzzer.common import file_reader as fr


def main():
    properties = fr.read_properties("reachability")
    print(properties)


if __name__ == '__main__':
    main()
