#!/bin/bash

readonly FRR_IMAGE="prefrr.tar"

echo "1/2 Load FRR image"
docker load -i ${FRR_IMAGE}

echo "2/2 Setting up FRR container"
docker run -itd --privileged --name frr --network host frr:6.0.2
