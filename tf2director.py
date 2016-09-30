#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
from configparser import ConfigParser

from tf2server import Tf2Server


class ServerConfigurationError(Exception):
    """
    Raised when user tries to used improperly configured TF2 server.
    """
    pass


class ServerInvalidPathError(Exception):
    """
    This exception is raised if the specified server path is invalid (i.e. does not contain a valid TF2 server
    installation or does not exist at all).
    """
    pass


def main():
    """
    Parse command line options, read config and run desired action.
    """
    description = 'tf2director is a script that helps managing multiple Team Fortress 2 server instances.'

    parser = ArgumentParser(description=description)
    parser.add_argument('server', help='server to be used', metavar='server')
    parser.add_argument('action', choices=['start', 'stop'], help='action to do', metavar='action')

    args = parser.parse_args()

    home = os.path.expanduser('~')
    config_file = os.path.join(home, 'tf2director.ini')
    if not os.path.isfile(config_file):
        print('Config file missing (' + config_file + ')')
        sys.exit(1)

    config = ConfigParser()
    config.read(config_file)

    if args.server not in config:
        raise ServerConfigurationError()

    server_name = args.server
    server_path = os.path.expanduser(config[args.server]['path'])
    server = Tf2Server(server_name, server_path)

    if args.action == 'start':
        ip = config[args.server]['ip']
        port = config[args.server]['port']
        initial_map = config[args.server]['initial_map']
        cfg_file = config[args.server]['server_config']

        server.start(ip, port, initial_map, cfg_file)

    elif args.action == 'stop':
        server.stop()

if __name__ == '__main__':
    main()
