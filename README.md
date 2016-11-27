Salt Masterful Architecture on Google Compute Engine
============================================================

The project setups the Salt master (on Ubuntu VM) and Salt minions (on both Ubuntu VM and Windows VM).
It should be used for educational purpose. Therefore, you should look at the source code and learn how it works.


Installation
---------------

1. Install virtualenv's environment with `virtualenv ENV`.
2. Load the virtualenv's environment with `source ENV/bin/activate`.
3. Install dependencies with `pip install -r requirements.txt`.


Setup Google Compute Enginer Project
-------------------------------------

1. Go to [cloud.google.com/console](https://cloud.google.com/console) and creat a project.
2. Go to [Networking > External IP addresses](https://pantheon.corp.google.com/networking/addresses/list) and set up one external static address for the master in the correct zone.
3. Set `PROJECT`, `ZONE`, and `MASTER_IP_ADDRESS` in `handler.py` accordingly.


Usage
-------

1. Create the private-public key pair for the master with `python remote.py gen_keys --path . --name master`.
2. Create salt-master with `python remote.py create_master`.
3. Create an ubuntu minion with `python remote.py create_minion salt-ubuntu-minion-1`.
4. Create a windows minion with `python remote.py create_minion salt-windows-minion-1`.
5. SSH into the master with `gcloud compute ssh salt-master --project PROJECT` and ping all minions with `sudo salt '*' test.ping`.


FAQ
-----

### Why do we generate the master's key pair locally?

Because we want to be able to recreate the master with the same key pair.

In an opposed scenario, if we didn't have and use the same master's key pair, then we would need to update all minions to recognize the new master's key pair.


### Why do we generate the minion's key pair locally before creating the minion VM?

Because we can immediately add the minion public key to the master's accepted key list.

Otherwise, we would wait for the minion VM to start and ssh in to grab the public key. That could take a few more minutes.

In addition to that, we can't SSH into Windows, so we can't go that way for Windows.


### Why don't we use the bootstrap script from [salt-bootstrap](https://github.com/saltstack/salt-bootstrap)?

Because we want everything to be checked into our version control.And we want code that we can understand. We actually have learned a lot from salt-bootstrap and take only what we need.


### How is this different from salt-cloud?

There are two main differences:

1. salt-cloud doesn't support creating a master.
2. To create a minion, salt-cloud needs to be run on salt-master. Therefore, salt-master must have SSH privilege to all minions. This can be tricky in certain situations (e.g. sshing requires touching a USB security key and typing a password.)


Author
------
Tanin Na Nakorn ([@tanin](https://twitter.com/tanin))

