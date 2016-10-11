#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
from configparser import ConfigParser

import actions
from tf2server import Tf2Server


def main():
    """
    Parse command line options, read config and run desired action.
    """
    description = 'tf2director is a script that helps managing multiple Team Fortress 2 server instances.'

    parser = ArgumentParser(description=description)
    parser.add_argument('server', help='server to be used or "all"', metavar='server')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'console', 'update', 'report'],
                        help='action to do', metavar='action')

    args = parser.parse_args()

    home = os.path.expanduser('~')
    config_file = os.path.join(home, 'tf2director.ini')
    if not os.path.isfile(config_file):
        print('Config file missing (' + config_file + ')')
        sys.exit(1)

    config = ConfigParser()
    config.read(config_file)

    if 'all' in config:
        raise ValueError('A server cannot be named \'all\'!')

    if args.server not in config and args.server != 'all':
        raise ValueError('Server \'{0}\' is not configured'.format(args.server))

    servers = []

    if args.server == 'all':
        for s in config.sections():
            c = config[s]
            server = Tf2Server(s, os.path.expanduser(c['path']))
            server.ip = c['ip']
            server.port = c['port']
            server.initial_map = c['initial_map']
            server.cfg_file = c['server_config']

            servers.append(server)
    else:
        c = config[args.server]
        path = c['path']
        server = Tf2Server(args.server, os.path.expanduser(path))
        server.ip = c['ip']
        server.port = c['port']
        server.initial_map = c['initial_map']
        server.cfg_file = c['server_config']

        servers.append(server)

    try:
        if args.action == 'start':
            actions.start(servers)

        elif args.action == 'stop':
            actions.stop(servers)

        elif args.action == 'restart':
            actions.restart(servers)

        elif args.action == 'console':
            if len(servers) == 1:
                server = servers[0]
                server.attach()

        elif args.action == 'update':
            actions.update(servers)

        elif args.action == 'report':
            actions.report(servers)

    except ValueError as error:
        print('{0}'.format(error))


if __name__ == '__main__':
    main()
