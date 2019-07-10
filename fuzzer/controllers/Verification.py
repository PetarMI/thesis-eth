from termcolor import colored as clr
from fuzzer.verifiers import reach_ping_verifier as rpv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Verification:
    # TODO make this pass the correct properties to every ver function
    # currently contains only reachability properties anyway
    def __init__(self, properties: dict, fuzz_data: FuzzData):
        self.properties = properties
        self.fuzz_data = fuzz_data
        self.iterations = -1
        self.num_violations = 0

    def verify_ping_reachability(self) -> dict:
        return rpv.verify_ping_reachability(self.properties)

    def verify_fib_reachability(self, state):
        print(clr("## Property checking", 'cyan'))
        failed_nets: list = self.fuzz_data.get_link_nets(state)
        property_failures: dict = rfv.verify_fib_reachability(self.properties,
                                                              self.fuzz_data,
                                                              failed_nets)
        print(clr("## Final verdict", 'cyan'))
        rfv.examine_violations(state, property_failures)

        self.update_logs(property_failures)

        print(clr("## Applying changes to fuzzed properties", 'cyan'))
        self._remove_properties(property_failures)

    def stop_fuzzing(self) -> bool:
        return len(self.properties.keys()) == 0

    def update_logs(self, property_failures: dict):
        self.iterations += 1
        self.num_violations += len(property_failures.keys())

        with open(const.VIOLATIONS_LOG, "a+") as logfile:
            logfile.write("{},{}\n".format(self.iterations, self.num_violations))

    @staticmethod
    def interpret_ping_results(ping_results: dict):
        rpv.interpret_verification_results(ping_results)

    def _remove_properties(self, property_failures: dict):
        for property_id in property_failures.keys():
            removed_property = self.properties.pop(property_id, None)

            if removed_property:
                print(clr("Removed property with ID {} from further verification".
                          format(property_id), 'green'))
            else:
                print(clr("Tried to remove property with non-existing ID {}".
                          format(property_id), 'red'))
