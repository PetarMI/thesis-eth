#!/bin/bash

echo "1/2 Pulling FRR image"
docker pull petarmi/frr:6.0.2

echo "2/2 Setting up FRR container"
docker run -itd --privileged --name frr --network host petarmi/frr:6.0.2
