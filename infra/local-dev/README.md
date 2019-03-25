# Running local Simulator 

**THIS INFO IS A BIT OUTDATED**

### Setting up the infrastructure 

1. Build the images 
    ```bash
    cd /containers/phynet 
    docker build --rm -t phynet:1.0 .
    ```
    
    ```bash
    cd /containers/playmaker 
    docker build --rm -t playmaker:1.0 .
    ```

2. Create Playmaker container 

    ```bash
    docker run -dit /
    -v /var/run/docker.sock:/var/run/docker.sock /
    --mount type=bind,source=<path to folder with topologies>,target=/home/topologies / 
    --name pm playmaker:1.0
    ``` 

### Running on a specific topology

1. Inside `Playmaker` create a `docker-compose`

    ```bash
    python3 compose_generator.py -f /home/topologies/<project>/<project>.topo
    ```

2. Inside `Playmaker` create a `csv` file storing info about the current Docker container in the topology 

    ```bash
    python3 save_topo_data.py -f /home/topologies/<project>/<project>.topo
    ```

3. Execute `docker-compose` on host machine
    
    ```bash
    <project_path>/topologies/<project>/docker-compose up -d
    ```
    
4. Setup Layer 2 containers and network devices from inside the `Playmaker`

    ```bash
    /home/scripts/./topoSetup.sh
    ```
    