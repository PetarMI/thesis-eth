#!/bin/bash

readonly DOCKER_DATA=/home/net_state/dockers.csv
readonly FRR_SETUP_SCRIPT=/home/scripts/setupFRR.sh

readonly L_GREEN='\033[1;32m'
readonly GREEN='\033[0;32m'
readonly CYAN='\033[0;36m'
readonly RED='\033[0;31m'
readonly NC='\033[0m' # No Color

printf "${L_GREEN}##### Setup all Layer 2 containers${NC}\n"

pids=()

while IFS=, read -r name type
do
    printf "${GREEN}## Configuring container ${name}${NC}\n"
    docker exec ${name} ${FRR_SETUP_SCRIPT} &
    pids+=($!)
done < ${DOCKER_DATA}

echo "${#pids[@]}"
echo "Processing..."

# wait for all containers to finish setting up
for pid in ${pids[*]}; do
    wait $pid
done

printf "${L_GREEN}### Done ${NC}\n"

#awk -F, '
#{
#	printf("Executing setup\n")
#	system("docker >> out.txt")
#}
#' /home/net_state/dockers.csv
