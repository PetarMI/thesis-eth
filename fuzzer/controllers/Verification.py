from termcolor import colored as clr
from fuzzer.verifiers import reach_ping_verifier as rpv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.common.FuzzData import FuzzData


class Verification:
    # TODO make this pass the correct properties to every ver function
    # currently contains only reachability properties anyway
    def __init__(self, properties: dict, fuzz_data: FuzzData):
        self.properties = properties
        self.fuzz_data = fuzz_data

    def verify_ping_reachability(self) -> dict:
        return rpv.verify_ping_reachability(self.properties)

    def verify_fib_reachability(self, state):
        print(clr("## Property checking", 'cyan'))
        property_failures: dict = rfv.verify_fib_reachability(self.properties,
                                                              self.fuzz_data)
        print(clr("## Final verdict", 'cyan'))
        rfv.examine_violations(state, property_failures)

        print(clr("## Applying changes to fuzzed properties", 'cyan'))
        self._remove_properties(property_failures)

    def stop_fuzzing(self) -> bool:
        return len(self.properties.keys()) == 0

    @staticmethod
    def interpret_ping_results(ping_results: dict):
        rpv.interpret_verification_results(ping_results)

    def _remove_properties(self, property_failures: dict):
        for property_id in property_failures.keys():
            removed_property = self.properties.pop(property_id, None)

            if removed_property:
                print(clr("Removed property with ID from further verification".
                          format(property_id), 'green'))
            else:
                print(clr("Tried to remove property with non-existing ID {}".
                          format(property_id), 'red'))
