import os
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
        Creates the Tf2Server class instance that uses the given path.
        :param name: The TF2 server instance name.
        :param path: The absolute path to where the TF2 server is located.
        """
        self.name = name
        self.path = path
        self.tmux_server = None

        if not os.path.isdir(os.path.join(path, 'tf')):
            raise CorruptedTf2ServerInstanceError()

    def _get_tmux_session_name(self):
        file_name = os.path.join(self.path, '.tmux-session')
        if not os.path.isfile(file_name):
            return self.name
        else:
            with open(file_name, 'r') as f:
                content = f.read()
            return content.strip()

    def _get_log_file_path(self):
        return os.path.join(self.path, self.name.join('.log'))

    def is_running(self):
        """
        Checks whether the server is running or not.
        :return: True if the instance is running, False otherwise.
        """
        session_name = self._get_tmux_session_name()
        if not self.tmux_server:
            self.tmux_server = libtmux.Server()

        return self.tmux_server.has_session(session_name)

    def start(self, ip, port=27015, map='cp_badlands', server_cfg_file='server.cfg'):
        """
        Starts the server, if it is not yet running.
        """
        if self.is_running():
            print('Server already running')
        else:
            session = self.tmux_server.new_session(self._get_tmux_session_name())
            pane = session.attached_pane

            srcds_location = os.path.join(self.path, 'srcds_run')
            exec = '{0} -game tf -ip {1} -port {2} +map {3} +maxplayers 24 -secured -timeout 0 +servercfgfile {4}' \
                .format(srcds_location, ip, port, map, server_cfg_file)
            print(exec)
            pane.send_keys(exec)

    def stop(self):
        if self.is_running():
            self.tmux_server.kill_session(self._get_tmux_session_name())
