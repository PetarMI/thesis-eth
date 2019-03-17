# Debian9 Docker
This is a binary docker container build of debian9.

Dockerfile is copied from the official FRR repo 

Currently working but is not the best solution:

* built from packages
* hacky way of setting up the image through a not optimized Dockerfile

### Build
```
docker build --rm -t frr:6.0.2 .
```

### Running
```
docker run -itd --privileged --name frr frr:6.0.2
```

vtysh
```
docker exec -it frr vtysh
```
