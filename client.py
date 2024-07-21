#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/client.py
# Simple Zen-of-Python client that asks three questions then disconnects.

import argparse, random, socket, zen_utils, ssl

def client(address, cafile, cause_error=False):
    cxt = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=cafile)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    secure_sock = cxt.wrap_socket(sock, server_side=False, server_hostname=address[0])
    aphorisms = list(zen_utils.aphorisms)
    if cause_error:
        secure_sock.sendall(aphorisms[0][:-1])
        return
    for aphorism in random.sample(aphorisms, 3):
        secure_sock.sendall(aphorism)
        print(aphorism, zen_utils.recv_until(secure_sock, b'.'))
    secure_sock.close()
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('cafile', help='Provide a CA certificate for ssl connection')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.cafile, args.e)
