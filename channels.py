import threading
import pickle
import signal
import socket
import sys
import time
from threading import Lock
class Channel:

    def __init__(self, name: str) :

        self.name = name
        self.clients = [] # Clients who have joined the server
        self.lock = Lock()

    def add_client(self, client_socket):
        with self.lock:
            if client_socket not in self.clients:
                self.clients.append(client_socket)

    def remove_client(self, client_socket, server):
        print("getting lock")
        with self.lock:
            print("got lock")
            if client_socket in self.clients:
                self.clients.remove(client_socket)
        if self.clients:
            """When a user leaves the channel, it should alert others in the channel that they have left"""
            print("1")
            leaving_client_info = server.clients.get(client_socket, {})
            print("2")
            nickname = leaving_client_info.get('nickname', 'A user')
            print("3")
            self.broadcast(f"{nickname} has left the channel.", sender_socket=None)
        # Once the last client leaves, the server should have the channel be removed
        else:
            server.remove_channel(self.name)  # Notify the server to delete the channel

    def broadcast(self, message, sender_socket=None):
        with self.lock:
            for client in self.clients:
                if client != sender_socket: 
                    try:

                        self.send_object(client, {"type": "message", "data": message})

                    except: 

                        self.remove_client(client)

    def send_object(self, client_socket, data):
        try:
            client_socket.send(pickle.dumps(data))
        except:
            # Handle sending failure (e.g., client disconnected)
            self.remove_client(client_socket)