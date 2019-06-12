from fuzzer.verifiers import reachability_verifier as rv
from fuzzer.verifiers import reach_fib_verifier as rfv
from fuzzer.common.FuzzData import FuzzData

class Verification:
    # TODO make this pass the correct properties to every ver function
    # currently contains only reachability properties anyway
    def __init__(self, properties: list, fuzz_data: FuzzData):
        self.properties = properties
        self.fuzz_data = fuzz_data

    def verify_ping_reachability(self):
        rv.verify_ping_reachability(self.properties)

    def verify_fib_reachability(self):
        return rfv.verify_fib_reachability(self.properties, self.fuzz_data)

# def verify_properties(self, state: tuple):
#     ver_results: dict = self.verification.verify_ping_reachability()
#     all_successful: bool = True
#     failures = []
#
#     for property_id, ver_res in ver_results.items():
#         if ver_res["status"] == 0:
#             continue
#         else:
#             all_successful = False
#
#         col, desc = pretty_print_failure(property_id, ver_res)
#         failures.append({
#             "pid": property_id,
#             "state": state,
#             "desc": desc,
#         })
#
#         print(clr(desc, col))
#
#     if all_successful:
#         print(clr("All properties HOLD", 'green'))
#
#     fw.write_state_failures(failures)
#
# def pretty_print_failure(pid: int, verification_res: dict):
#     ver_status = verification_res["status"]
#
#     if ver_status == 1:
#         return 'red', "Property {} FAILED: {}".format(pid, verification_res["desc"])
#     if ver_status == 2:
#         return 'yellow', "Property {} WARNING: {}".format(pid, verification_res["desc"])
#     if ver_status == 3:
#         return 'grey', "Property {} ERROR: {}".format(pid, verification_res["desc"])
