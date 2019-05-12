# Master Thesis at ETH Zurich SS2019

## Project structure

    ├── infra                   # Network Simulator implementation
    ├── fuzzer                  # Logic for fuzzer
    ├── synth                   # Scripts for synthesizing test networks
    ├── topologies              # Topology files
    ├── deprecated              # Old code which is not used anymore
    └── requirements.txt        # venv modules for running the python scripts
    └── README.md

## Prerequisites 

### Virtual environment

The python scripts require a `python3` virtual environment which contains all 
dependencies specified in `requirements.txt`. To prepare the environment:
 
 1. Create a virtual environment inside a dir of choice
    * `virtualenv venv`
    * `python3 -m venv <venv-name>`
 2. Activate environment
    * `. <path_to_venv>/venv/bin/activate`
 3. Install required modules
    * `pip install -r requirements.txt`
 4. Add project dir to `PYTHONPATH`
    * `export PYTHONPATH=~/thesis-eth`
    
### Running tests
   
Every dir may have a `tests` subfolder. To run those tests go into the dir 
containing the `tests` folder and execute:
   
* `python -m pytest tests/ -v`