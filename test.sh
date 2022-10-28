#!/bin/bash

docker=$1

case "$docker" in
        "tf_2.8") formal_docker_image="tensorflow/tensorflow:2.8.0-gpu-jupyter"
        ;;
        "tf_2.7") formal_docker_image="tensorflow/tensorflow:2.7.0-gpu-jupyter"
        ;;
esac

echo $formal_docker_image

