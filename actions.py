from tf2server import Tf2Server


def start(servers):
    """
    Start the server(s) with the config provided.
    :param servers: list of servers to be started
    """
    for s in servers:
        if not isinstance(s, Tf2Server):
            raise TypeError('Not an instance of Tf2Server')

        s.start()


def stop(servers):
    """
    Stop the server(s), quitting them properly.
    :param servers: list of servers to be stopped.
    """
    for s in servers:
        if not isinstance(s, Tf2Server):
            raise TypeError('Not an instance of Tf2Server')

        s.stop()


def restart(servers):
    """
    Stop and then start each server on the list.
    :param servers: list of servers to be started
    """
    for s in servers:
        if not isinstance(s, Tf2Server):
            raise TypeError('Not an instance of Tf2Server')

        s.stop()
        s.start()


def update(servers):
    """
    Show down servers, update them and restart.
    This function updates only these servers that require it (i.e. are out-of-date).
    :param servers: list of servers to be updated.
    :return:
    """
    for s in servers:
        if not isinstance(s, Tf2Server):
            raise TypeError('Not an instance of Tf2Server')

        if s.is_running() and s.has_update():
            s.stop()
            s.update()
            s.start()
        elif not s.is_running():
            s.update()


def status(servers):
    """
    Print server(s) status.
    :param servers:  list of servers.
    :return:
    """
    for s in servers:
        if not isinstance(s, Tf2Server):
            raise TypeError('Not an instance of Tf2Server')

        s.print_status()
