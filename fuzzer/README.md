# Fuzzer

    ├── common                  # File reading and writing, constants
    ├── controllers             # Fuzzing logic
    ├── executors               # Scripts for interacting with the running containers
    ├── verifiers               # Logic for checking properties
    └── README.md
    
## Running the fuzzer

Currently the fuzzer only works for reachability properties. To run:

1. Prepare for fuzzing
    * `./prepare_fuzzing.sh` - Gets the data of the running containers
2. Parse the reachability properties and generate instructions for the executor
    * `python reachability_parser.py`
3. Execute the ping
    * `./reachability_exec.sh`
4. Verify pings are successful
    * `python reachability_verifier.py`