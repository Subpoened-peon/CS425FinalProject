import socket
import threading
import pickle
import sys

class Client:
    def __init__(self):
        self.client = None
        self.connected = False
        self.channels = [] # Channels the client is a member of.
        self.nickname = None
        self.current_channel = None

    def add_channel(self, channel_name):
        """Limit number of channels a client can be a part of to 10 like the RFC1459 suggests"""
        if len(self.channels) >= 10:
            print(f"You are a part of 10 channels already. Please leave one to join this channel.")
            return False
        if channel_name not in self.channels:
            self.channels.append(channel_name)
            return True
        else:
            print(f"Current Channel: '{channel_name}'.")
            return False
        
    def remove_channel(self, channel_name):
        """Remove a channel from the client's list through leave"""
        if channel_name in self.channels:
            self.channels.remove(channel_name)
            print(f"Left channel: {channel_name}")
        else:
            print(f"Not in channel '{channel_name}'.")

    def send_object(self, data):
        if self.client.fileno() == -1:
            print("Unexpected closed socket, you have been disconnected")
            self.connected = False
            return
        try:
            self.client.send(pickle.dumps(data))
        except:
            self.client.close()
            self.connected = False
            print("Unexpected closed socket, you have been disconnected")

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
                self.client.close()
                break

    def connect_to_server(self, server_name, port):
        """After using the connect command."""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((server_name, int(port)))
            self.connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            print(f"Connected to {server_name}:{port}.")
        except Exception as e:
            print(f"Failed to connect to {server_name}:{port}. Error: {e}")

    def disconnected_mode(self):
        """When first logging in, or disconnecting from a server, handle client here"""
        print("Client ready. Use '/help' for commands.")
        while not self.connected:
            command = input("> ").strip()
            if command.startswith("/"):
                parts = command.split(" ", 5)
                cmd = parts[0][1:]
                args = parts[1:] if len(parts) > 1 else []
                
                if cmd == "connect":
                    if len(args) == 0:
                        print("Usage: /connect <server-name> [port#]")
                    else:
                        server_name = args[0]
                        port = args[1] if len(args) > 1 else 12345
                        self.connect_to_server(server_name, port)
                elif cmd == "help":
                    print("Available Commands:")
                    print("/connect <server-name> [port] - Connect to a server")
                    print("/quit - Exit the client")
                    print("/help - Show this help message")
                elif cmd == "quit":
                    print("Exiting client.")
                    return False
                else:
                    print(f"Unknown command: {cmd}. Use /help for a list of commands.")
            else:
                print("Connect to a server before sending messages.")
        return True

    def connected_mode(self):
        """Handle client commands when connected to a server."""
        print("Connected to server. Use '/help' for server commands.")
        while self.connected:
            command = input("> ").strip()
            if command.startswith("/"):
                parts = command.split(" ", 5)
                cmd = parts[0][1:]
                args = parts[1:] if len(parts) > 1 else []
                
                if cmd == "quit":
                    self.send_object({"command": cmd})
                    print("Disconnected from server.")
                    self.client.close()
                    self.connected = False
                elif cmd == "following":
                    self.send_object({"command": cmd})
                else:
                    self.send_object({"command": cmd, "args": args})
            else:
                self.send_object({"command": None, "message": command})

    def start(self):
        """Main client loop."""
        while True:
            if not self.connected:
                if not self.disconnected_mode():
                    break
            else:
                self.connected_mode()

if __name__ == "__main__":
    client = Client()
    client.start()
