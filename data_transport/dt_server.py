#! /usr/bin/env python
# _*_coding:utf-8 -*_
import socketserver
import socket
import time
import threading

client_addr_list = []
client_sock_list = []


class DTServerHandler(socketserver.BaseRequestHandler):
    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip+":"+str(port)+" is connect!")

        client_addr_list.append(ip)
        client_sock_list.append(self.request)
        print(client_addr_list)

    def handle(self):
        while True:
            data = str(self.request.recv(1024), 'utf-8')
            if data:
                cur_thread = threading.current_thread()
                response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
                self.request.sendall(response)
            time.sleep(1)

    def finish(self):
        print("client is disconnect")
        client_addr_list.remove(self.client_address)
        client_sock_list.remove(self.request)


class DTServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def sendall(self,message):
        data = bytes(message,'utf-8')
        if client_addr_list:
            for client in client_sock_list:
                client.sendall(data)


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'utf-8'))
        response = str(sock.recv(1024), 'utf-8')
        print("Received: {}".format(response))


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = DTServer((HOST, PORT), DTServerHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    client1 = threading.Thread(target=client, args=(ip ,port, "Hello World 1"))
    client1.start()
    # client1.join()
    time.sleep(1)
    server.sendall("From server")

    server.shutdown()
    server.server_close()
