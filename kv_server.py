'''
this is doc string of kv_server
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SocketServer
import threading
import sys
import getopt


class KVHandler(SocketServer.StreamRequestHandler):
    ''' KVHandler is used for handling stream request
    '''
    def handle(self):
        #self.data = self.rfile.readline().strip()
        self.data = self.rfile.readline().strip().split()
        print "%s wrote:" % self.client_address[0]
        #print "================\r\n", self.data, "\r\n================"
        #self.datas=os.popen(self.data).read()
        if self.data[0] in ("SET", "set"):
            self.datas = "OK"
            DB[self.data[1]] = self.data[2]
        elif self.data[0] in ("GET", "get"):
            self.datas = DB.get(self.data[1])
        self.wfile.write(str(self.datas))

if __name__ == '__main__':
    try:
        OPTS, ARGS = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
    except getopt.GetoptError:
        sys.exit()

    HOST = "localhost"
    PORT = 5678
    DB = {}

    for name, val in OPTS:
        if name in ("-h", "--host"):
            HOST = val
        elif name in ("-p", "--port"):
            PORT = int(val)

    try:
        SERVER = SocketServer.ThreadingTCPServer((HOST, PORT), KVHandler)
        SERVER_THREAD = threading.Thread(target=server.serve_forever)
        SERVER_THREAD.setDaemon(True)
        SERVER_THREAD.start()
        SERVER.serve_forever()
        SERVER.shutdown()
    except Exception, e:
        print Exception, ":", e
        exit(1)
