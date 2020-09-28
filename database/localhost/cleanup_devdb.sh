#!/bin/sh

docker kill dev_db_dbs_1
docker rm dev_db_dbs_1
sudo rm -r ./gitignore