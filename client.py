import socket
import threading
import pickle
import sys

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channels = []

    def add_channel(self, channel_name):
        """Limit number of channels a client can be a part of to 10 like the RFC1459 suggests"""
        if len(self.channels) >= 10:
            print(f"You are a part of 10 channels already. Please leave one to join this channel.")
            return False
        if channel_name not in self.channels:
            self.channels.append(channel_name)
            return True
        else:
            print(f"Already in channel '{channel_name}'.")
            return False
        
    def remove_channel(self, channel_name):
        """Remove a channel from the client's list through leave"""
        if channel_name in self.channels:
            self.channels.remove(channel_name)
            print(f"Left channel: {channel_name}")
        else:
            print(f"Not in channel '{channel_name}'.")
    
    def send_object(self, data):
        self.client.send(pickle.dumps(data))

    def receive_messages(self):
        while True:
            try:
                data = pickle.loads(self.client.recv(1024))
                if data['type'] == "message":
                    print(data['data'])
                elif data['type'] == "error":
                    print(f"Error: {data['data']}")
                elif data['type'] == "success":
                    print(f"Success: {data['data']}")
                elif data['type'] == "update":
                    if data['action'] == "remove_channel":
                        self.remove_channel(data['channel'])
            except:
                print("Disconnected from server.")
                self.client.close()
                break

    def start(self, server_name, port):
        try:
            self.client.connect((server_name, port))
            print("Connected to the server.")
            threading.Thread(target=self.receive_messages, daemon=True).start()

            while True:
                command = input()
                if command.startswith("/"):
                    parts = command.split(" ", 1)
                    cmd = parts[0][1:]
                    args = parts[1:] if len(parts) > 1 else []
                    self.send_object({"command": cmd, "args": args})
                    if cmd == "quit":
                        break
                else:
                    self.send_object({"command": None, "message": command})
        except:
            print("Failed to connect to server.")
        finally:
            self.client.close()

if __name__ == "__main__":
    server_name = input("Enter server name (default: localhost): ") or "localhost"
    port = int(input("Enter port number (default: 12345): ") or 12345)
    client = Client()
    client.start(server_name, port)
