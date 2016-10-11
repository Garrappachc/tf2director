from tf2server import Tf2Server


def try_update(server):
    """
    Check whether there is an update available for the server. If there is, report it to the admin(s).
    :param server: instance of Tf2Server
    """
    if not isinstance(server, Tf2Server):
        raise TypeError

    status = 'not running'
    if server.is_running():
        if server.has_update():
            status = 'HAS UPDATE'
        else:
            status = 'no update'

    print('{0}: {1}'.format(server.name, status))
