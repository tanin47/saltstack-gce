import re
import os
import tempfile
import shutil

from fabric import api
from salt import crypt
from salt import utils


PROJECT = 'test-salt-tanin'
ZONE = 'us-west1-a'
MASTER_IP_ADDRESS = '104.198.15.98'


MASTER_INSTANCE_NAME = 'salt-master'


def get_host_user_and_ssh_key_path(instance_name, project, zone):
  output = api.local(gcloud('compute ssh %s --dry-run' % instance_name),
                     capture=True)
  print output

  m = re.match('/usr/bin/ssh -i ([^ ]+)(?: -o [^ ]+)* ([^ ]+)@([^ ]+)', output)

  return (m.group(3), m.group(2), m.group(1))


def gcloud(cmd):
  """Return a gcloud command with proper flags."""
  return 'gcloud {cmd} --project "{project}" --zone "{zone}" --quiet'.format(**
      {'cmd': cmd, 'project': PROJECT, 'zone': ZONE})


def create_master():
  """Create a windows instance with the name."""
  pem, pub, _ = read_keys('.', 'master')

  startup_script = tempfile.NamedTemporaryFile(delete=False)
  with open('master-startup.sh') as f:
    startup_script.write(f.read().format(pem=pem, pub=pub))
  startup_script.close()

  try:
    api.local(gcloud('compute instances delete "%s" --delete-disks all' % MASTER_INSTANCE_NAME))
  except SystemExit:
    pass

  api.local(gcloud('compute instances create "%s" --machine-type "n1-standard-1" --subnet "default" --maintenance-policy "MIGRATE" --scopes default="https://www.googleapis.com/auth/cloud-platform" --image "/ubuntu-os-cloud/ubuntu-1610-yakkety-v20161020" --boot-disk-size "50" --boot-disk-type "pd-standard" --boot-disk-device-name "%s" --metadata-from-file startup-script=%s --address %s' % (MASTER_INSTANCE_NAME, MASTER_INSTANCE_NAME, startup_script.name, MASTER_IP_ADDRESS)))

  os.remove(startup_script.name)


def gen_keys(path, name):
  """Generate a pair of public-private key into path."""
  crypt.gen_keys(path, name, 2048)

  print 'Finger: %s' % utils.pem_finger(os.path.join(path, name + '.pub'))
  print 'Public key: %s' % os.path.join(path, name + '.pub')
  print 'Private key: %s' % os.path.join(path, name + '.pem')


def read_keys(path, name):
  pem, pub, finger  = '', '', ''

  with open(os.path.join(path, name + '.pem')) as f:
    pem = f.read()
  with open(os.path.join(path, name + '.pub')) as f:
    pub = f.read()
  finger = utils.pem_finger(os.path.join(path, name + '.pub'))

  return pem, pub, finger


def get_generated_keys():
  """Generate a pair of public-private key and return as a tuple."""
  tmpdir = tempfile.mkdtemp()
  name = 'dontcare'

  gen_keys(tmpdir, name)

  pem, pub, finger  = read_keys(tmpdir, name)
  shutil.rmtree(tmpdir)

  return pem, pub, finger


def put_content_on_master(content, target_file):
  """Put content on master."""
  (host, username, ssh_key_file_path) = get_host_user_and_ssh_key_path(
        MASTER_INSTANCE_NAME, PROJECT, ZONE)

  api.env.host_string = '%s@%s' % (username, host)
  api.env.key_filename = ssh_key_file_path
  api.env.use_shell = False

  with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
    tmpfile.write(content)

  api.put(tmpfile.name, target_file, use_sudo=True)
  os.remove(tmpfile.name)


class Config(object):
  """Represents config of an instance."""

  def __init__(self, script_arg, script_template_path, image_name):
    self.script_arg = script_arg
    self.script_template_path = script_template_path
    self.image_name = image_name


def get_config(name):
  """Get config given the instance name."""
  if 'windows' in name:
    return Config('windows-startup-script-ps1',
                  'windows-minion-startup.ps1',
                  '/windows-cloud/windows-server-2012-r2-dc-v20161115')
  else:
    return Config('startup-script',
                  'linux-minion-startup.sh',
                  '/ubuntu-os-cloud/ubuntu-1610-yakkety-v20161020')


def create_minion(name):
  """Create a linux minion given the name."""
  minion_pem, minion_pub, _ = get_generated_keys()
  put_content_on_master(minion_pub, '/etc/salt/pki/master/minions/' + name)

  _, _, master_finger = read_keys('.', 'master')
  config = get_config(name)

  startup_script = tempfile.NamedTemporaryFile(delete=False)
  with open(config.script_template_path) as f:
    startup_script.write(f.read().format(
        pem=minion_pem, pub=minion_pub, master_finger=master_finger,
        name=name, master_ip_address=MASTER_IP_ADDRESS))
  startup_script.close()

  try:
    api.local(gcloud('compute instances delete "%s" --delete-disks all' % name))
  except SystemExit:
    pass

  api.local(gcloud('compute instances create "%s" --machine-type "n1-standard-1" --subnet "default" --maintenance-policy "MIGRATE" --scopes default="https://www.googleapis.com/auth/cloud-platform" --image %s --boot-disk-size "50" --boot-disk-type "pd-standard" --boot-disk-device-name "%s" --metadata-from-file %s=%s' % (name, config.image_name, name, config.script_arg, startup_script.name)))

  os.remove(startup_script.name)

