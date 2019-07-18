from termcolor import colored as clr
from fuzzer.controllers.fib import Fib
from fuzzer.verifiers import reach_ping_verifier as rpv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.verifiers import iso_fib_verifier as ifv
from fuzzer.common.FuzzData import FuzzData


class Verification:
    def __init__(self, properties: dict, fib: Fib, fuzz_data: FuzzData):
        self.reach_props = properties.get("reachability", dict())
        self.iso_props = properties.get("isolation", dict())
        self.fib = fib
        self.fuzz_data = fuzz_data
        self.iso_iterations = -1
        self.reach_iterations = -1

    def verify_ping_reachability(self) -> dict:
        return rpv.verify_ping_reachability(self.reach_props)

    def verify_fib_properties(self, state):
        print(clr("## Updating FIB", 'cyan'))
        self.fib.update_fib()

        self._verify_fib_reachability(state)
        self._verify_fib_isolation(state)

    def _verify_fib_reachability(self, state):
        print(clr("## Reachability property checking", 'cyan'))
        if len(self.reach_props.keys()) == 0:
            print("No more Reachability properties")
            return

        failed_nets: list = self.fuzz_data.get_link_nets(state)
        self.reach_iterations += 1

        property_failures: dict = rfv.verify_fib_reachability(self.reach_props,
                                                              self.fuzz_data,
                                                              failed_nets)
        print(clr("## Final verdict", 'cyan'))
        rfv.examine_violations(state, self.reach_iterations, property_failures)

        print(clr("## Applying changes to reachability properties", 'cyan'))
        remove_properties(property_failures, self.reach_props)

    def _verify_fib_isolation(self, state):
        print(clr("## Isolation property checking", 'cyan'))
        if len(self.iso_props.keys()) == 0:
            print("No more Blacklisting properties")
            return

        failed_nets: list = self.fuzz_data.get_link_nets(state)
        self.iso_iterations += 1

        property_failures: dict = ifv.verify_fib_isolation(self.iso_props,
                                                           self.fib,
                                                           self.fuzz_data,
                                                           failed_nets)
        print(clr("## Final verdict", 'cyan'))
        ifv.examine_violations(state, self.iso_iterations, property_failures)

        print(clr("## Applying changes to blacklist properties", 'cyan'))
        remove_properties(property_failures, self.iso_props)

    def stop_fuzzing(self) -> bool:
        if len(self.reach_props.keys()) == 0 and len(self.iso_props.keys()) == 0:
            return True

        return False

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
