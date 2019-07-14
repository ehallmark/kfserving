#!/bin/bash -e

export GOPATH="$HOME/go"
export PATH="${PATH}:${GOPATH}/bin"
export KO_DOCKER_REPO='docker.io/ehallmark1122'

cd "$GOPATH/src/github.com/kubeflow/kfserving/python"

sudo ./build_model_initializer.sh
sudo ./build_sklearnserver.sh

cd ../

make deploy-dev
