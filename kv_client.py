#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
kv_client.py mimics redis client
running w/o args, will entering interactive mode
exit w/ ctrl+d
'''

import socket
import sys

HOST = 'localhost'
PORT = 5678
BUFSIZ = 4096
ADDR = (HOST, PORT)
IS_INTERACTIVE = len(sys.argv) < 2
EXIT_NO = 0
INPUT_DATA = ""

while True:
    if IS_INTERACTIVE:
        try:
            INPUT_DATA = raw_input('> ').strip()
        except EOFError as msg:
            print msg
            sys.exit(0)
        if INPUT_DATA == "":
            print "no input, bye!"
            sys.exit(1)
    else:
        INPUT_DATA = " ".join(sys.argv[1:])

    TCPSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        TCPSOCK.connect(ADDR)
        TCPSOCK.send('%s\r\n' % INPUT_DATA)
        RECV_DATA = TCPSOCK.recv(BUFSIZ)
        if not RECV_DATA:
            print "wrong input"
            EXIT_NO = 1
        print RECV_DATA.strip()
    except socket.error:
        print "woops, socket err"
    finally:
        TCPSOCK.close()
        if not IS_INTERACTIVE:
            sys.exit(EXIT_NO)
