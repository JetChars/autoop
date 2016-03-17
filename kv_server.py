#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
kv_server mimics redis server
'''

import SocketServer
import threading
import sys
import getopt
import re


class KVHandler(SocketServer.StreamRequestHandler):
    '''
    KVHandler is used for handling stream request
    '''
    def handle(self):
        self.data = self.rfile.readline().strip().split()
        self.result = ""
        if self.data[0] in ("SET", "set"):
            if len(self.data) == 3:
                DB[self.data[1]] = self.data[2]
                self.result = "OK"
        elif self.data[0] in ("GET", "get"):
            self.result = DB.get(self.data[1], "")
        elif self.data[0] in ("AUTH", "auth"):
            if AUTH.get(self.data[1]) == self.data[2]:
                self.result = "OK"
        self.wfile.write(str(self.result))



if __name__ == '__main__':
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
    except getopt.GetoptError as msg:
        print "wrong arguments"
        print msg
        sys.exit(1)

    HOST = "localhost"
    PORT = 5678
    DB = {}
    AUTH = {}

    for name, val in OPTS:
        if name in ("-h", "--host"):
            HOST = val
        elif name in ("-p", "--port"):
            PORT = int(val)

    with open("auth.conf") as auth_file:
        for eachline in auth_file.readlines():
            if not re.search('^#', eachline):
                usr = eachline.strip().split()
                AUTH[usr[0]] = usr[1]

    SERVER = SocketServer.ThreadingTCPServer((HOST, PORT), KVHandler)
    SERVER_THREAD = threading.Thread(target=SERVER.serve_forever)
    SERVER_THREAD.setDaemon(True)
    SERVER_THREAD.start()
    SERVER.serve_forever()
    SERVER.shutdown()
    SERVER.server_close()


