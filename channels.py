import threading
import pickle

class Channel:

    def __init__(self, name: str) :

        self.name = name
        self.clients = [] # Clients who have joined the server
        """ self.lock = threading """ # add later for threading?

    def add_client(self, client_socket):

        if client_socket not in self.clients:
            self.clients.append(client_socket)

    def remove_client(self, client_socket, server):
 
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            
            # Once the last client leaves, the server should have the channel be removed
            if len(self.clients) == 0:
                self.broadcast(f"Channel {self.name} is being deleted as it has no more users.", sender_socket=None)
                server.remove_channel(self.name)  # Notify the server to delete the channel

    def broadcast(self, message, sender_socket=None):

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