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
    socket = context.socket(zmq.DEALER)
    identity = u'client-2'
    socket.identity = identity.encode('ascii')
    socket.connect('tcp://localhost:5570')
    print 'Client %s started' % (identity)
    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)
    reqs = 0
    count=0
    while True:
        reqs = reqs + 1
        print 'Req #%d sent..' % (reqs)
        socket.send_string(u'request #%d' % (reqs))
        for i in range(5):
            sockets = dict(poll.poll(100))
            if socket in sockets:
                msg = socket.recv()
                count = count + 1
                print 'Client %s received: %s count %d' % (identity, msg, count)

    socket.close()
    context.term()

if __name__ == "__main__":
    main()