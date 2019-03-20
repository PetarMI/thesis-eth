#!/bin/bash

while IFS=, read -r col1 col2
do
    docker exec ${col1} "/home/scripts/setupFRR.sh"
done < /home/net_state/dockers.csv


#awk -F, '
#{
#	printf("Executing setup\n")
#	system("docker >> out.txt")
#}
#' /home/net_state/dockers.csv
