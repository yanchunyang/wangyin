#!/usr/bin/python
"""
Created on Fri Nov 23 13:23:39 2012

@author: wavelet liu
"""

import SocketServer, subprocess, sys
from threading import Thread
from optparse import OptionParser
import sys
import os
from sets import Set
import datetime 
import shutil
import time
sys.path.append("E:\\后百度时代\\Pythoncode\\")
import forecast_read

#Refer: http://docs.python.org/release/2.5.2/lib/optparse-standard-option-actions.html
usage = "usage: ./TestAutomatinClient.py [options]"
parser = OptionParser(usage=usage, add_help_option=False)
parser.add_option("--help", action="help", help="Show this help message and exit")
parser.add_option("-v", action="store_true", dest="debug", help="print out debug information")
parser.add_option("--smppSimulateServer", dest="smppSimulateServer", help="Specify remote smppSimulateServer hostname or ip")
parser.add_option("--smppSimulateServerPort", dest="smppSimulateServerPort", help="Specify remote smppSimulateServer port")

(options, args) = parser.parse_args()

if options.smppSimulateServer == None:    
    HOST = 'localhost'    # The remote host
else:
    HOST = options.smppSimulateServer

PORT = 55555
    

# This is the protocol part.   
def process_command(data,smppServer):
    print 'command=',data
    import json
    decoded = json.loads(data)
 
    command=decoded['command']    
    if command.lower().find("start") != -1:
        return forecast_read.sumbytime()
        #return 'got you'
    '''    
    elif command.lower().find("stop") != -1:
        StopSMPPSimulatorClient()
        return "Stopped successfully"
    elif command.lower().find("ping") != -1:
        return "Ping OK"
  
    else:
        return  'Invalid command:'+command '''

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        #import pdb; pdb.set_trace(); 
        smppServer=self.request.getpeername()[0]
        print '[Received Request from]: ',smppServer
        data = self.request.recv(1024)  # clip input at 1Kb
        reply = process_command(data,smppServer)
        if reply is not None:
            self.request.send(str(reply))

        print 'sleep for 20 seconds to demo multiple client handling..'
        time.sleep(20)
        print 'Done'

        self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    forecast_read.readline()

    print 'Server started and listen in port {}'.format(PORT)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
