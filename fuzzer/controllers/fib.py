import json
import subprocess
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Fib:
    def __init__(self, fuzz_data: FuzzData):
        self.fib = dict()
        self.dev2vm = fuzz_data.get_dev2vm()

    def update_fib(self):
        for dev, vm in self.dev2vm.items():
            fib: str = exec_get_fib(vm, dev)
            parsed_fib: dict = json.loads(fib)
            print(parsed_fib.keys())


def exec_get_fib(vm_ip, src_dev) -> str:
    result = subprocess.run([const.FIB_INFO_SH, vm_ip, src_dev],
                            stdout=subprocess.PIPE)

    return result.stdout.decode('utf-8')
