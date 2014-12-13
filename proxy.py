#!/usr/bin/env python

from LoggingProxyHTTPHandler import LoggingProxyHTTPHandler
import BaseHTTPServer
import sys


def main(args):
    try:
        port = int(args[1])
    except IndexError:
        port = 8000
    server_address = ('', port)
    httpd = BaseHTTPServer.HTTPServer(server_address, LoggingProxyHTTPHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
