from termcolor import colored as clr
from fuzzer.controllers.fib import Fib
from fuzzer.verifiers import reach_ping_verifier as rpv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.verifiers import iso_fib_verifier as ifv
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Verification:
    def __init__(self, properties: dict, fib: Fib, fuzz_data: FuzzData):
        self.reach_props = properties.get("reachability", dict())
        self.iso_props = properties.get("isolation", dict())
        self.fib = fib
        self.fuzz_data = fuzz_data

    def verify_ping_reachability(self) -> dict:
        return rpv.verify_ping_reachability(self.reach_props)

    def verify_fib_reachability(self, state):
        print(clr("## Reachability property checking", 'cyan'))
        failed_nets: list = self.fuzz_data.get_link_nets(state)
        property_failures: dict = rfv.verify_fib_reachability(self.reach_props,
                                                              self.fuzz_data,
                                                              failed_nets)
        print(clr("## Final verdict", 'cyan'))
        rfv.examine_violations(state, property_failures)

        print(clr("## Applying changes to fuzzed properties", 'cyan'))
        remove_properties(property_failures, self.reach_props)

    def verify_fib_isolation(self, state):
        print(clr("## Isolation property checking", 'cyan'))
        failed_nets: list = self.fuzz_data.get_link_nets(state)
        self.fib.update_fib()

        property_failures: dict = ifv.verify_fib_isolation(self.reach_props,
                                                           self.fib,
                                                           self.fuzz_data,
                                                           failed_nets)
        print(clr("## Final verdict", 'cyan'))
        ifv.examine_violations(state, property_failures)

        print(clr("## Applying changes to fuzzed properties", 'cyan'))
        remove_properties(property_failures, self.iso_props)

    def stop_fuzzing(self, fuzz_type: str) -> bool:
        if fuzz_type == const.REACH_FUZZ:
            return len(self.reach_props.keys()) == 0
        elif fuzz_type == const.ISO_FUZZ:
            return len(self.iso_props.keys()) == 0
        else:
            raise ValueError("Unsupported fuzzing type {}".format(fuzz_type))

    @staticmethod
    def interpret_ping_results(ping_results: dict):
        rpv.interpret_verification_results(ping_results)


def remove_properties(property_failures: dict, properties: dict):
    for property_id in property_failures.keys():
        removed_property = properties.pop(property_id, None)

        if removed_property:
            print(clr("Removed property with ID {} from further verification".
                      format(property_id), 'green'))
        else:
            print(clr("Tried to remove property with non-existing ID {}".
                      format(property_id), 'red'))
