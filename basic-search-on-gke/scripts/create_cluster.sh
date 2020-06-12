#!/bin/bash
# Copyright 2018 Yahoo Holdings. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.
set -euo pipefail
set -x

CLUSTER_NAME=${1:-"vespa"}
ZONE=${2:-"europe-west1-b"}
MACHINE_TYPE=${3:-"n1-standard-4"}
NB_NODES=${6:-3}



gcloud container clusters create $CLUSTER_NAME --zone $ZONE --num-nodes=$NB_NODES --machine-type=$MACHINE_TYPE
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE
