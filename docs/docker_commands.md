##### Container lifecycle
* docker create --interactive --tty --name <container name> <img name>:<img tag>
    * example: `docker create -it --name simple-ubuntu ubuntu:late`
    * Additional OPTIONS: `--volume`, `--ip`, `--network <net name>`, `--hostname -h`
* docker start --interactive <container name>

##### Docker networking
* `docker network ls`
* docker network inspect <network name>
* docker network create --driver <bridge/host/none> <network name>
* docker network rm <network name>
* docker network connect <net name> <container name>
* docker network disconnect <net name> <container name>

##### Container management
* docker inspect <container name>
* docker inspect <container name> -f "{{json .NetworkSettings.Networks }}"

##### Container sessions 
* docker attach <container name>
* docker exec -it <container id> bash
* To detach from the container1 container and leave it running, use the keyboard sequence `CTRL-p CTRL-q`

##### Docker Hub
* docker tag <image name> <username/repository:tag>

##### Services
* docker stack deploy -c <.yml file> <stack name>
* `docker service ls` OR docker stack services <service name>
    * see the services that are running OR on a specific stack
* docker service ps <service name>
    * see the tasks for a specific service
* docker stack ps <stack name> 
    * see the tasks/containers running on the specified stack


##### Docker Machine
* `docker-machine create --driver virtualbox myvm1`
* `docker-machine ls`
* docker-machine ssh < vm> < command>


##### Installing stuff
* `apt-get update
   apt-get install net-tools`
  `apt-get install iputils-ping`
