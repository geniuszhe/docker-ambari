#!/bin/bash

: ${AMBARI_HOST:=$AMBARISERVER_PORT_8080_TCP_ADDR}
: ${BLUEPRINT:=single-node-hdfs-yarn}

echo AMBARI_HOST=${AMBARI_HOST:? ambari server address is mandatory, fallback is a linked containers exposed 8080}

./wait-for-host-number.sh
./hosts_gen.py

curl -i -H "X-Requested-By: ambari" -u admin:admin -X PUT -d'{ "Repositories" : { "base_url":"http://10.0.83.123/HDP/2.x/updates/2.6.1.0/", "verify_base_url":true }}' http://localhost:8080/api/v1/stacks/HDP/versions/2.6/operating_systems/redhat7/repositories/HDP-2.6

curl -i -H "X-Requested-By: ambari" -u admin:admin -X PUT -d'{"Repositories" : { "base_url":"http://10.0.83.123/HDP-UTILS-1.1.0.21/repos/centos7/","verify_base_url":true }}' http://localhost:8080/api/v1/stacks/HDP/versions/2.6/operating_systems/redhat7/repositories/HDP-UTILS-1.1.0.21

java -jar ambari-shell.jar --ambari.host=$AMBARI_HOST
