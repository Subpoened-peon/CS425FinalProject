import socket
import threading
import pickle
import sys
import signal
from time import time

class Server:
    def __init__(self, port=12345, debug_level=0):
        self.host = 'localhost'
        self.port = port
        self.debug_level = debug_level
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.clients = {}  # {client_socket: {'nickname': nickname, 'channel': channel}}
        self.channels = {}  # {channel_name: [client_sockets]}
        self.shutdown_time = time() + 180  # Idle timeout (3 minutes)

    def debug(self, message):
        """Print debug messages based on the debug level."""
        if self.debug_level > 0:
            print(message)

    def send_object(self, client_socket, data):
        """Send a Python object to the client."""
        client_socket.send(pickle.dumps(data))

    def receive_object(self, client_socket):
        """Receive a Python object from the client."""
        return pickle.loads(client_socket.recv(1024))

    def broadcast(self, message, channel, sender_socket=None):
        """Send a message to all clients in a channel."""
        for client in self.channels.get(channel, []):
            if client != sender_socket:
                try:
                    self.send_object(client, {"type": "message", "data": message})
                except:
                    self.remove_client(client)

    def remove_client(self, client_socket):
        """Remove a client from the server."""
        if client_socket in self.clients:
            info = self.clients.pop(client_socket)
            nickname = info['nickname']
            channel = info['channel']
            if channel in self.channels and client_socket in self.channels[channel]:
                self.channels[channel].remove(client_socket)
                self.broadcast(f"{nickname} has left the channel.", channel)
        client_socket.close()

    def handle_client(self, client_socket):
        """Handle communication with a single client."""
        self.shutdown_time = time() + 180  # Reset idle timer
        nickname = None
        current_channel = None

        try:
            self.debug(f"Client connected: {client_socket.getpeername()}")
            self.send_object(client_socket, {"type": "message", "data": "Welcome! Use /help for commands."})

            while True:
                data = self.receive_object(client_socket)
                command = data.get("command")
                args = data.get("args", [])

                if command == "nick":
                    nickname = args[0]
                    if nickname in [info['nickname'] for info in self.clients.values()]:
                        self.send_object(client_socket, {"type": "error", "data": "Nickname already in use."})
                    else:
                        self.clients[client_socket] = {"nickname": nickname, "channel": None}
                        self.send_object(client_socket, {"type": "success", "data": f"Nickname set to {nickname}"})

                elif command == "join":
                    channel = args[0]
                    if current_channel:
                        self.channels[current_channel].remove(client_socket)
                        self.broadcast(f"{nickname} has left the channel.", current_channel)
                    current_channel = channel
                    self.clients[client_socket]['channel'] = current_channel
                    self.channels.setdefault(channel, []).append(client_socket)
                    self.broadcast(f"{nickname} has joined the channel.", current_channel)
                    self.send_object(client_socket, {"type": "success", "data": f"Joined channel {channel}"})

                elif command == "list":
                    channels_info = "\n".join([f"{ch}: {len(members)} users" for ch, members in self.channels.items()])
                    self.send_object(client_socket, {"type": "message", "data": channels_info})

                elif command == "leave":
                    if current_channel:
                        self.channels[current_channel].remove(client_socket)
                        self.broadcast(f"{nickname} has left the channel.", current_channel)

                        """Remove the channel from the clients channel list"""
                        self.send_object(client_socket, {"type": "update", "action": "remove_channel", "channel": current_channel})

                        current_channel = None

                        self.clients[client_socket]['channel'] = None
                    self.send_object(client_socket, {"type": "success", "data": "Left the channel."})

                elif command == "quit":
                    break

                elif command == "help":
                    help_text = (
                        "/nick <nickname>: Set your nickname\n"
                        "/join <channel>: Join a channel\n"
                        "/list: List all channels and the number of users\n"
                        "/leave: Leave the current channel\n"
                        "/quit: Disconnect\n"
                    )
                    self.send_object(client_socket, {"type": "message", "data": help_text})

                else:
                    if current_channel:
                        self.broadcast(f"{nickname}: {data.get('message')}", current_channel, sender_socket=client_socket)
                    else:
                        self.send_object(client_socket, {"type": "error", "data": "Join a channel to chat."})

        except Exception as e:
            self.debug(f"Error: {e}")
        finally:
            self.remove_client(client_socket)

    def start(self):
        print(f"Server started on {self.host}:{self.port}")
        signal.signal(signal.SIGINT, self.graceful_shutdown)

        while True:
            if time() > self.shutdown_time:
                print("Server idle for 3 minutes. Shutting down.")
                self.graceful_shutdown(None, None)

            try:
                client_socket, client_address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except:
                pass

    def graceful_shutdown(self, signum, frame):
        print("Shutting down server.")
        for client in self.clients.keys():
            client.close()
        self.server.close()
        sys.exit(0)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("-p", type=int, default=12345, help="Port number")
    parser.add_argument("-d", type=int, choices=[0, 1], default=0, help="Debug level (0: errors, 1: all events)")

    args = parser.parse_args()

    server = Server(port=args.p, debug_level=args.d)
    server.start()
