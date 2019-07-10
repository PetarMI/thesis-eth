from subprocess import call
from termcolor import colored as clr
from ttictoc import TicToc
import logging
import json
from fuzzer.controllers import property_parser as pp
from fuzzer.controllers.Statespace import Statespace
from fuzzer.controllers import StateTransition
from fuzzer.controllers import Verification as Ver
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Fuzzer:
    def __init__(self):
        # declare all state variables used during fuzzing
        self.search_plan: list = None
        self.search_stats: dict = None
        self.transition = None
        self.verification = None

    def prepare_fuzzing(self, depth: int):
        # define necessary variables
        fuzz_data = FuzzData()
        nets: list = fuzz_data.get_ospf_networks()
        statespace = Statespace(depth, nets)
        properties: dict = pp.parse_properties(fuzz_data)

        self.logger = logging.getLogger('fuzzer')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('{}/{}_h.log'.format(const.LOG_DIR, fuzz_data.get_topo_name()), mode='a+')
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

        # set fuzzing approach state variables
        t = TicToc()
        t.tic()
        self.search_plan = statespace.get_heuristic_plan(properties, fuzz_data)
        self.search_stats = statespace.get_fuzzing_stats()
        self.transition = StateTransition.PartialRevert(fuzz_data)
        self.verification = Ver.Verification(properties, fuzz_data)
        t.toc()
        self.logger.info("prep,{}".format(t.elapsed))

    def verify_deployment(self):
        print(clr("#### Verifying deployment", 'cyan', attrs=['bold']))
        exec_ping_reachability()
        ping_results: dict = self.verification.verify_ping_reachability()
        self.verification.interpret_ping_results(ping_results)

    def fuzz(self):
        t = TicToc(nested=True)

        for n, state in enumerate(self.search_plan):
            t.tic()
            print(clr("State {}/{}: {}".format(n, self.search_stats["total"], state),
                      'green', attrs=['bold']))

            print(clr("#### Executing state transition", 'cyan', attrs=['bold']))
            t.tic()
            self.transition.perform_state_transition(state)
            t.toc()
            self.logger.info("otransition,{}".format(t.elapsed))

            print(clr("#### Verifying properties", 'cyan', attrs=['bold']))
            t.tic()
            self.verification.verify_fib_reachability(state)
            t.toc()
            self.logger.info("over,{}".format(t.elapsed))

            if self.check_stop_fuzzing(n):
                break

            t.toc()
            self.logger.info("state,{}".format(t.elapsed))

            print("===================================")

    def print_search_strategy(self):
        print(clr("## Statespace stats", 'magenta', attrs=['bold']))
        print(json.dumps(self.search_stats, indent=4))

    def get_search_plan(self) -> list:
        return self.search_plan

    def check_stop_fuzzing(self, n: int) -> bool:
        if self.verification.stop_fuzzing():
            print(clr("#### Finished fuzzing after {} iterations".format(n),
                      'green', attrs=['bold']))
            return True

        return False


def exec_ping_reachability():
    return_code: int = call([const.PING_SH])
    signal_script_fail(return_code)


def signal_script_fail(return_code: int, msg="", die=False):
    if return_code:
        err_msg = "Failed to ".format(msg) if msg else "Fail"
        print(clr(err_msg, 'red'))

        if die:
            exit(return_code)
