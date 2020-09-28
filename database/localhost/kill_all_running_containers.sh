#!/bin/sh

docker kill $(docker container ls -a -q)
