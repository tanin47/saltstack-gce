#! /bin/bash

read -r -d '' PEM <<- EOM
{pem}
EOM

read -r -d '' PUB <<- EOM
{pub}
EOM

mkdir -p /etc/salt/pki/master/ \
  && echo "$PEM" > /etc/salt/pki/master/master.pem \
  && chmod 400 /etc/salt/pki/master/master.pem \
  && echo "$PUB" > /etc/salt/pki/master/master.pub \
  && wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add - \
  && mkdir -p /etc/apt/sources.list.d \
  && echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' >> /etc/apt/sources.list.d/saltstack.list \
  && apt-get update -y \
  && apt-get install -y salt-master

