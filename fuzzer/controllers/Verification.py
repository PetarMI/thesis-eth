from fuzzer.verifiers import reach_ping_verifier as rpv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.common.FuzzData import FuzzData


class Verification:
    # TODO make this pass the correct properties to every ver function
    # currently contains only reachability properties anyway
    def __init__(self, properties: list, fuzz_data: FuzzData):
        self.properties = properties
        self.fuzz_data = fuzz_data

    def verify_ping_reachability(self) -> dict:
        return rpv.verify_ping_reachability(self.properties)

    def verify_fib_reachability(self) -> dict:
        return rfv.verify_fib_reachability(self.properties, self.fuzz_data)

    @staticmethod
    def interpret_ping_results(ping_results: dict):
        rpv.interpret_verification_results(ping_results)

    @staticmethod
    def interpret_fib_results(state: tuple, fib_results: dict):
        rfv.interpret_verification_results(state, fib_results)
