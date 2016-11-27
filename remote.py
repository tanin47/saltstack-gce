import argparse
import inspect
import paramiko

from fabric import api

import handler


paramiko.util.log_to_file('paramiko.log')
api.env.connection_attempts = 3
api.env.timeout = 3


def _args_to_dict(args, method):
  """Convert args to dict that is compatible with the method's argument."""
  arg_names = inspect.getargspec(method).args
  args_dict = {
      k: v
      for k, v in vars(args).items() if k in arg_names and v is not None
  }
  return args_dict


def main():
  """Parse the command-line args and invoke the right command."""
  parser = argparse.ArgumentParser(
      description='Remote helps you with remote command-line tasks.')
  subparsers = parser.add_subparsers(dest='command')

  subparsers.add_parser(
      'deploy', help='Deploy the state to salt-master.')
  subparsers.add_parser(
      'create_master', help='Create the salt-master instance')

  parser_gen_keys = subparsers.add_parser(
      'gen_keys', help='Generate a private-public key for the master to use.')
  parser_gen_keys.add_argument('-p', '--path')
  parser_gen_keys.add_argument('-n', '--name')

  parser_create_minion = subparsers.add_parser(
      'create_minion', help='Create a salt-minion.')
  parser_create_minion.add_argument(
      'name', help='The name of the salt-minion.')

  args = parser.parse_args()
  method = getattr(handler, args.command)
  method(**_args_to_dict(args, method))


if __name__ == '__main__':
  main()
