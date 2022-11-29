#!/bin/bash

DOCKER_REPO=doublehub/ntpc_tad_bot
BASE_DIR=$(dirname "$0")
PROJECT_DIR=$(cd "$BASE_DIR/.."; pwd -P)

docker build $PROJECT_DIR \
    -t "$DOCKER_REPO"