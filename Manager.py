#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from Worker import Worker

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


def main():
    # Cria um Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Escutando na porta %s ...' % SERVER_PORT)
    running(server_socket)


def running(server_socket):
    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        print("Nova requisicao ->", client_address)
        worker = Worker(client_connection, client_address)
        worker.start()

    # Close socket
    server_socket.close()


if __name__ == '__main__':
    main()
