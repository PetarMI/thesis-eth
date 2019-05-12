### Dir structure
    ├── cisco                   # Logic for translating Cisco configs to FRR
    ├── common                  # file reading and writing
    ├── seq_synth               # Topology files
    └── README.md

### Running

To translate a Cisco topology to FRR run:

```bash
python cisco_translator -t <topo-name>
```