#!/usr/bin/python
"""
Created on Fri Nov 23 13:02:31 2012

@author: wavelet liu
"""
import socket
import sys
from optparse import OptionParser

#########################################################
##                      Parse options                   #
#########################################################
#Refer: http://docs.python.org/release/2.5.2/lib/optparse-standard-option-actions.html
usage = "usage: ./TCPClient.py [options]"
parser = OptionParser(usage=usage, add_help_option=False)
parser.add_option("--help", action="help", help="Show this help message and exit")
parser.add_option("--start", action="store_true", dest="start", default=True,help="Ask client to start to send traffic")
parser.add_option("--stop", action="store_true", dest="stop", default=False,help="Ask client to stop to send traffic")
parser.add_option("-t", dest="test_type", help="Test Type: one of submit_sm, query_sm,delivery_sm, cancel_sm,ALL, STRESS")
parser.add_option("-n", dest="number", help="Run how many times")
parser.add_option("--ping", action="store_true", dest="ping", default=False,help="Ping Client")
parser.add_option("--remoteIP", dest="remoteIP", help="Specify remote server ip")
parser.add_option("-v", action="store_true", dest="debug", help="print out debug information")

(options, args) = parser.parse_args()

if options.remoteIP == None:    
    HOST = 'localhost'    # The remote host
else:
    HOST = options.remoteIP
    
PORT = 55555              # The same port as used by the server

def encode_json(data):
    import json
    data_string = json.dumps(data)
    print 'ENCODED:', data_string
    return data_string
    
def StartSMPPClient():
    print "[StartSMPPClient...]"
     # Generate dictionary
    data = {}
    data['forecasttime'] = "2013-04"
    data['currenttime']="2013-03"
    data['op']=['zhixiao','qudao']
    data['field']=['16','32']
    data['rrequest']='0'
    count=1    
    if options.number != None:
        count=int(options.number)

    #data['parameter'] = 'test parameter'
    
    sock=connectToRemote(HOST,PORT)    
    ret=sendCommandToRemote(sock,data)
    return
    
def StopSMPPClient():
    data = {}
    data['command'] = "stop"
    
    sock=connectToRemote(HOST,PORT)    
    ret=sendCommandToRemote(sock,data)
    return

def PingRemote():
    print "[PingRemote...]"
     # Generate dictionary
    data = {}
    data['command'] = "ping"
    
    try:
        sock=connectToRemote(HOST,PORT)    
        ret=sendCommandToRemote(sock,data)
    except socket.error as msg:
        print "Ping failed:", msg
        return

def connectToRemote(HOST,PORT):
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    
    if s is None:
        print 'could not open socket'
        sys.exit(1)
    return s
    
def sendCommandToRemote(socket, data): 
    socket.sendall(encode_json(data))
    data = socket.recv(1024)
    socket.close()
    print '[Received return msg]:', repr(data)
    
if __name__ == "__main__":
    if options.stop == True:
        StopSMPPClient()
    elif options.ping == True:
        PingRemote()
    elif options.start == True:
        StartSMPPClient()
    
        
    print "Done"
