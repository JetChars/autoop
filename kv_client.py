#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import sys

HOST='localhost'
PORT=5678
BUFSIZ = 4096
ADDR = (HOST, PORT)

if len(sys.argv) < 2:
    while True:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        try:
            tcpCliSock.connect(ADDR)
            data = raw_input('> ')
            if not data:
                break
            tcpCliSock.send('%s\r\n' % data)
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            print data.strip()
        except Exception, e:
            print Exception, ":", e
            exit(1)
        finally:
            tcpCliSock.close()
else:
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    try:
        tcpCliSock.connect(ADDR)
        data = " ".join(sys.argv[1:])
        if not data:
            exit(0)
        tcpCliSock.send('%s\r\n' % data)
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            exit(0)
        print data.strip()
    except Exception, e:
        print Exception, ":", e
        exit(1)
    finally:
        tcpCliSock.close()

