import logging
import os
import socket
import sys
from functools import partial, update_wrapper


class ExecutionLock(object):
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, objtype):
        return partial(self.__call__, obj)

    def __call__(self, *args, **kwargs):
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as sock:
            script = os.path.realpath(sys.argv[0])
            try:
                sock.bind('\0' + script)
                return self.func(*args, **kwargs)
            except socket.error:
                logging.warning(
                    'Another execution of the script is processing. Exiting...'
                )
                return
