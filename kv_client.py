#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
kv_client.py mimics redis client
'''

import socket
import sys

HOST = 'localhost'
PORT = 5678
BUFSIZ = 4096
ADDR = (HOST, PORT)
IS_INTERACTIVE = len(sys.argv) < 2
EXIT_NO = 0
# ERRORS

while True:
    TCPSOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        TCPSOCK.connect(ADDR)
        if IS_INTERACTIVE:
            INPUT_DATA = raw_input('> ')
        else:
            INPUT_DATA = " ".join(sys.argv[1:])
        if not INPUT_DATA:
            print "no input, bye!"
            break
        TCPSOCK.send('%s\r\n' % INPUT_DATA)
        INPUT_DATA = TCPSOCK.recv(BUFSIZ)
        if not INPUT_DATA:
            print "wrong input"
            EXIT_NO = 1
        print INPUT_DATA.strip()
    except socket.error as msg:
        print "woops, socket err"
        # print msg
    finally:
        TCPSOCK.close()
        if not IS_INTERACTIVE:
            sys.exit(EXIT_NO)
