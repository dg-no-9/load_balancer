#!/usr/bin/env python
"""
The front end of storage layer that handles the store request from the
collection layer
"""

import time
import struct
from pylib.wiring import gevent_zmq as zmq
import pylib.fastjson as json

from pylib import logger, conf
from pylib import wiring
from Queue import Queue

log = logger.getLogger(__name__)

def main():
    """main function"""
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind('tcp://*:5570')

    backend = context.socket(zmq.DEALER)
    backend.bind('tcp://*:5571')

    poll = zmq.Poller()
    poll.register(frontend, zmq.POLLIN)
    poll.register(backend,  zmq.POLLIN)

    while True:
        sockets = dict(poll.poll())
        if frontend in sockets:
            ident, msg = frontend.recv_multipart()
            print 'Server received %s id %s' % (msg, ident)
            backend.send_multipart([ident, msg])
        if backend in sockets:
            ident, msg = backend.recv_multipart()
            print 'Sending to frontend %s id %s' % (msg, ident)
            frontend.send_multipart([ident, msg])

    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    main()