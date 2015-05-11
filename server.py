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
	context=zmq.Context()
	worker = context.socket(zmq.DEALER)
	worker.connect('tcp://localhost:5571')
	print 'Worker started'

	receiver = context.socket(zmq.PULL)
	receiver.bind('tcp://*:5503')

	poll = zmq.Poller()
	poll.register(worker, zmq.POLLIN)
	poll.register(receiver,  zmq.POLLIN)
	identifier=""
	queue = Queue(0)
	count = 0
	while True:
		sockets = dict(poll.poll(10))
		if receiver in sockets:
			msg = receiver.recv()
			print 'Received Msg: %s' % (msg)
			queue.put(msg)
		if worker in sockets:
			ident, req_msg = worker.recv_multipart()
			print 'Worker received %s from %s' % (req_msg, ident)
        # replies = randint(0,4)
        # for i in range(replies):
        #     time.sleep(1. / (randint(1,10)))
			if not queue.empty():
				msg = queue.get()
				queue.task_done()	
				worker.send_multipart([ident, msg])
				count = count + 1

	worker.close()

if __name__ == "__main__":
	main()

