#!/bin/sh

../staging_cluster/use-cluster.sh

ssh-keygen -q -f ./id_rsa -N "" -C staging_automarker
ssh-keyscan github.com >> known_hosts


kubectl delete secret github-ssh-key-secret 

kubectl create secret generic github-ssh-key-secret --from-file=id_rsa=id_rsa --from-file=id_rsa.pub=id_rsa.pub --from-file=known_hosts=known_hosts

cat id_rsa.pub 

rm id_rsa
rm id_rsa.pub
rm known_hosts
