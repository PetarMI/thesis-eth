from fuzzer.verifiers import reachability_verifier as rv
from fuzzer.verifiers import reach_fib_verifier as rfv

class Verification:
    # TODO make this pass the correct properties to every ver function
    # currently contains only reachability properties anyway
    def __init__(self, properties: list):
        self.properties = properties

    def verify_ping_reachability(self):
        rv.verify_ping_reachability(self.properties)

    def verify_fib_reachability(self):
        rfv.verify_ping_reachability(self.properties)
