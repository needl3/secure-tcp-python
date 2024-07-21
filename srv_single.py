#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_single.py
# Single-threaded server that serves one client at a time; others must wait.

import argparse
import ssl
import zen_utils

CA_FILE = "backend.crt"
PEM_FILE = "localhost.pem"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=300,
                        help='TCP port (default 3000)')
    args = parser.parse_args()
     
    # address = zen_utils.parse_command_line('simple single-threaded server')
    listener = zen_utils.create_srv_socket((args.host, args.p))
    cxt = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=CA_FILE)
    cxt.load_cert_chain(PEM_FILE)
    zen_utils.accept_connections_forever(listener, cxt)
