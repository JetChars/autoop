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
import urllib
from contextlib import closing



class KVHandler(SocketServer.StreamRequestHandler):
    '''
    KVHandler is used for handling stream request
    '''
    KV_DB = {}
    URL_DB = {}
    AUTH = {}
    IS_USER = False

    @staticmethod
    def load_conf():
        """
        load auth config
        """
        with open("auth.conf") as auth_file:
            for eachline in auth_file.readlines():
                if not re.search('^#', eachline):
                    usr = eachline.strip().split()
                    KVHandler.AUTH[usr[0]] = usr[1]

    def handle(self):
        self.data = self.rfile.readline().strip().split()
        self.result = ""
        if self.data[0] in ("SET", "set"):
            if len(self.data) == 3:
                KVHandler.KV_DB[self.data[1]] = self.data[2]
                self.result = "OK"
        elif self.data[0] in ("GET", "get"):
            self.result = KVHandler.KV_DB.get(self.data[1], "")
        elif self.data[0] in ("AUTH", "auth"):
            if KVHandler.AUTH.get(self.data[1]) == self.data[2]:
                self.result = "OK"
                KVHandler.IS_USER = True
        elif self.data[0] in ("URL", "url") and KVHandler.IS_USER:
            if KVHandler.URL_DB.has_key(self.data[1]):
                self.result = str(KVHandler.URL_DB[self.data[1]])
            else:
                with closing(urllib.urlopen(self.data[2])) as page:
                    url_result = [len(page.read()), page.code]
                    KVHandler.URL_DB[self.data[1]] = url_result
                    self.result = str(url_result)
        self.wfile.write(self.result)



if __name__ == '__main__':
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
    except getopt.GetoptError as msg:
        print "wrong arguments"
        print msg
        sys.exit(1)

    HOST = "localhost"
    PORT = 5678

    for name, val in OPTS:
        if name in ("-h", "--host"):
            HOST = val
        elif name in ("-p", "--port"):
            PORT = int(val)

    KVHandler.load_conf()

    SERVER = SocketServer.ThreadingTCPServer((HOST, PORT), KVHandler)
    SERVER_THREAD = threading.Thread(target=SERVER.serve_forever)
    SERVER_THREAD.setDaemon(True)
    SERVER_THREAD.start()
    SERVER.serve_forever()
    SERVER.shutdown()
    SERVER.server_close()


