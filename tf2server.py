import os
import time
import libtmux


class CorruptedTf2ServerInstanceError(Exception):
    """
    Raised when an invalid TF2 server instance is found.
    """


class Tf2Server(object):
    """
    The Tf2Server class represents a single Team Fortress 2 server.
    """

    def __init__(self, name, path):
        """
        Create the Tf2Server class instance that uses the given path.
        :param name: The TF2 server instance name.
        :param path: The absolute path to where the TF2 server is located.
        """
        self.name = name
        self.path = path
        self.tmux_server = None

        if not os.path.isdir(os.path.join(path, 'tf')):
            raise CorruptedTf2ServerInstanceError()

    @property
    def tmux_session_name(self):
        file_name = os.path.join(self.path, '.tmux-session')
        if not os.path.isfile(file_name):
            return 'tf2server_{0}_console'.format(self.name)
        else:
            with open(file_name, 'r') as f:
                content = f.read()
            return content.strip()

    @property
    def log_file_path(self):
        return os.path.join(self.path, self.name.join('.log'))

    def _has_sourcemod(self):
        path = os.path.join(self.path, 'tf/addons/sourcemod/plugins/basechat.smx')
        return os.path.isfile(path)

    def command(self, command):
        """
        Execute a command on the running TF2 server instance.
        :param command: str
        """
        if not self.is_running():
            return

        session = self.tmux_server.find_where({'session_name': self.tmux_session_name})
        pane = session.attached_pane

        print(command)
        pane.send_keys(command)

    def is_running(self):
        """
        Check whether the server is running or not.
        :return: True if the instance is running, False otherwise.
        """
        if not self.tmux_server:
            self.tmux_server = libtmux.Server()

        return self.tmux_server.has_session(self.tmux_session_name)

    def start(self, ip, port=27015, map='cp_badlands', server_cfg_file='server.cfg'):
        """
        Starts the server, if it is not yet running.
        """
        if self.is_running():
            print('Server already running')
        else:
            session = self.tmux_server.new_session(self.tmux_session_name)
            pane = session.attached_pane

            pane.cmd('-o', '/usr/bin/cat >> {0}'.format(self.log_file_path))

            srcds_location = os.path.join(self.path, 'srcds_run')
            command = '{0} -game tf -ip {1} -port {2} +map {3} +maxplayers 24 -secured -timeout 0 +servercfgfile {4}' \
                .format(srcds_location, ip, port, map, server_cfg_file)
            print(command)
            pane.send_keys(command)

    def stop(self, delay=10):
        """
        Show in-game notification, wait for the specified delay period and quit the server.
        :param delay: How long to wait before the server actually quits.
        """
        if self.is_running():
            msg = 'Server shutting down in {0} seconds!'.format(delay)
            print(msg)
            if self._has_sourcemod():
                self.command('sm_csay "{0}"'.format(msg))
            self.command('say "{0}"'.format(msg))

            time.sleep(delay)
            self.command('quit')
            time.sleep(5)

            self.tmux_server.kill_session(self.tmux_session_name)

        else:
            print('Server not running')

