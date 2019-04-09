#!/bin/bash

echo "1/3 Copying config files to FRR container"
config_file=$(hostname)
docker cp /home/configs/${config_file}.conf frr:/home/device-config.conf

echo "2/3 Setting configs to frr.conf"
docker exec frr bash -c "cp /home/device-config.conf /etc/frr/frr.conf"

echo "3/3 Restart FRR container to load new configs"
docker restart frr