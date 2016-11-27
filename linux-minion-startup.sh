#! /bin/bash

read -r -d '' PEM <<- EOM
{pem}
EOM

read -r -d '' PUB <<- EOM
{pub}
EOM

read -r -d '' MINION_CONFIG <<- EOM
master: "{master_ip_address}"
master_finger: "{master_finger}"
id: "{name}"
hash_type: sha256
EOM

mkdir -p /etc/salt/pki/minion \
 && echo "$PEM" > /etc/salt/pki/minion/minion.pem \
 && echo "$PUB" > /etc/salt/pki/minion/minion.pub \
 && chmod 400 /etc/salt/pki/minion/minion.pem \
 && wget -O - https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add - \
 && mkdir -p /etc/apt/sources.list.d \
 && echo 'deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main' >> /etc/apt/sources.list.d/saltstack.list \
 && apt-get update -y \
 && apt-get install -y salt-minion \
 && echo "$MINION_CONFIG" > /etc/salt/minion \
 && service salt-minion restart

