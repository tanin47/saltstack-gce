A masterful SaltStack architecture on Google Compute Engine
============================================================

A Fabric script to setup the Salt master (on Ubuntu VM) and Salt minions (on both Ubuntu VM and Windows VM).

This script should be used for educational purpose. Therefore, you should look at the source code and learn how it works.


Installation
---------------

1. Install virtualenv's environment with `virtualenv ENV`.
2. Load the virtualenv's environment with `source ENV/bin/activate`.
3. Install dependencies with `pip install -r requirements.txt`.


Setup Google Compute Enginer Project
-------------------------------------

1. Go to [cloud.google.com/console](https://cloud.google.com/console) and creat a project.
2. Go to [Networking > External IP addresses](https://pantheon.corp.google.com/networking/addresses/list) and set up one external static address for the master.
3. Set `PROJECT`, `ZONE`, and `MASTER_IP_ADDRESS` in `handler.py` accordingly.


Usage
-------

1. Create the private-public key pair for the master with `python remote.py gen_keys --path . --name master`.
2. Create salt-master with `python remote.py create_master`.
3. Create an ubuntu minion with `python remote.py create_minion salt-ubuntu-minion-1`.
4. Create a windows minion with `python remote.py create_minion salt-windows-minion-1`.
5. SSH into the master with `gcloud compute ssh salt-master --project PROJECT` and ping all minions with `sudo salt '*' test.ping`.


Author
------
Tanin Na Nakorn ([@tanin](https://twitter.com/tanin))

