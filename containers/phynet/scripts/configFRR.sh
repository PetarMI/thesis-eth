#!/bin/bash

echo "1/2 Copying config files to FRR container"
docker cp /home/configs/Qphynet1.conf frr:/home/device-config.conf

echo "2/2 Setting configs to frr.conf"
docker exec frr bash -c "cp /home/device-config.conf /etc/frr/frr.conf"