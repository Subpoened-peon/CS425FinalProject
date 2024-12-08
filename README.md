# CS425FinalProject
## Team Members
Jered Fennell - Nicholas Merritt - Atharva Pargaonkar

## Link to demo

https://youtu.be/VmY-dqbd0TE

## File/Folders Manifest

- **`server.py`**:
    This file implements a multithreaded chat server that allows clients to connect, set nicknames, and join or create channels for group communication. Each client is handled in a separate thread, enabling simultaneous interactions, while shared resources like client and channel data are protected using threading locks. The server supports commands like `/nick`, `/join`, `/leave`, and `/list`, facilitating channel management and message broadcasting, and includes idle timeout and graceful shutdown functionality.
    
- **`client.py`**:
    This file handles many things related to the client. Things like the client's list of channels that they are joined to. Clients have these key things:
    - **`nickname`**: This is assigned to the client after the nickname command. Each client is unique beforehand.

- **`channels.py`**:
    This file handles things related to the channels. It has a list of all the members that belong to it and a name. Channels have these key things:
    - **`name`**: This is assigned to the channel by the first client who joins it and is listed on the server.
    - **`clients`**: This is a list of all the clients who are members of the channel. When the last one leaves, the channel is removed.
    - **`thread`**

 ## Building
    1. Clone the Git repository
    2. Run the Server with the command : `python server.py`
    3. Run the Clients with the command : `python Client.py`
    
 ## Testing
 
### Manual Testing

A lot of testing was done manually. After making a change, we would start the server and the client, then connect to the default server on `localhost` at port `12345`.<br>
From there, we would test the adjusted commands, quit the session, and reconnect to verify persistence.<br>
Throughout this process, print statements helped confirm that the changes were functioning as intended. To check if multiple clients could use the same server and or channels, we would just have multiple instances of clients that connected/joined the same ones to use the messaging. 

 ## Reflections

 ### Nicholas Merritt
It was nice to try and do something fully in python. I had worked with some scripts that were given to students for larger java projects, but never had I written a full project in it. It took a while to understand it and I've come to learn that it has some similar functionality to javascript. Getting used to how objects and messages are passed around can be a bit confusing at first, but I find it very convenient now. 
 ### Atharva Pargaonkar
This project deepened my understanding of IRC-style communication and multithreaded server design. Implementing commands like /join, /nick, and /list helped me explore how chat protocols structure user interactions. Developing a multithreaded server taught me to manage multiple clients simultaneously, ensuring smooth and responsive communication.

 ### Jered Fennell
    This project was a strange one for me, I don't use python for anything so I hand to learn the semantics and what the language 
    required. I found the networking part of the project to be the least demanding, python makes sending data between the client 
    and server very easy. For handling many things, the requirements of the project I thought were weirdly outline in the project 
    specifications, and what was bing implemented from the course document, and what from the IRC protocol.
  
