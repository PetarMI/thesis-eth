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
    * see the tasks/contaners running on the specified stack

##### Installing stuff
* `apt-get update
   apt-get install net-tools`
  `apt-get install iputils-ping`
