import json
import subprocess
from fuzzer.common.FuzzData import FuzzData
from fuzzer.common import constants_fuzzer as const


class Fib:
    def __init__(self, fuzz_data: FuzzData):
        self.dev2vm = fuzz_data.get_dev2vm()
        self.fib = self.prepare_fib()

    def update_fib(self):
        for dev, vm in self.dev2vm.items():
            raw_fib: str = exec_get_fib(vm, dev)

            dev_fib: dict = self.parse_device_fib(raw_fib)
            self.fib.update({dev: dev_fib})

        print(json.dumps(self.fib, indent=4))

    @staticmethod
    def parse_device_fib(raw_fib: str) -> dict:
        parsed_fib: dict = json.loads(raw_fib)
        dev_fib = dict()

        for dest_network, prefix_data in parsed_fib.items():
            next_hops = []
            pdata = validate_prefix_data(prefix_data)
  
            if pdata["protocol"] == "ospf":
                for next_hop in pdata["nexthops"]:
                    next_hops.append(next_hop["ip"])
            
            dev_fib.update({dest_network: next_hops})

        return dev_fib

    def prepare_fib(self):
        fib = dict()

        for dev in self.dev2vm.keys():
            fib.update({dev: dict()})

        return fib


def exec_get_fib(vm_ip, src_dev) -> str:
    result = subprocess.run([const.FIB_INFO_SH, vm_ip, src_dev],
                            stdout=subprocess.PIPE)

    return result.stdout.decode('utf-8')


def validate_prefix_data(prefix_data: list) -> dict:
    if len(prefix_data) > 1:
        raise ValueError("Prefix data for some fib is larger than 1")
    
    return prefix_data[0]

