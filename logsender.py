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


log = logger.getLogger(__name__)

def main():
    """
    Main program loop where the storage listens for the incomming connection and
    from the collector layer, finds the appropriate Repo for the given log and
    forwards them to the RepoHandler.
    """
   
    zmq_context = zmq.Context()
    
    client_address = "PUSH:connect:tcp://127.0.0.1:5503"
    
    client_1 = wiring.create_wire(zmq_context, dict(format="json", socket=client_address))
    count=1
    msg="{'msg':'Hello World - 2'}"
    while True:
        
        client_1.send_raw(json.dumps(msg))
        if count == 100000:
            break
        count = count + 1
        #print json.loads(raw_data)
        print count

if __name__ == '__main__':
    main()
