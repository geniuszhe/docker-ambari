#!/bin/bash

./ambari-shell.sh << EOF
blueprint add --url https://raw.githubusercontent.com/geniuszhe/docker-ambari/master/blueprint/multi-node-hdfs-yarn
blueprint add --url https://raw.githubusercontent.com/geniuszhe/docker-ambari/master/blueprint/single-node-hdfs-yarn
cluster build --blueprint $BLUEPRINT
cluster autoAssign
cluster create --exitOnFinish true
EOF
