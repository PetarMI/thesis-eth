#!/bin/bash

echo "1/5 Pulling FRR image"
docker pull petarmi/frr:6.0.2

echo "2/5 Setting up FRR container"
docker run -itd --privileged --name frr --network host petarmi/frr:6.0.2

echo "3/5 Copying config files to FRR container"
config_file=$(hostname)
docker cp /home/configs/$config_file.conf frr:/home/device-config.conf

echo "4/5 Setting configs to frr.conf"
docker exec frr bash -c "cp /home/device-config.conf /etc/frr/frr.conf"

echo "5/5 Restart FRR container to load new configs"
docker restart frr
