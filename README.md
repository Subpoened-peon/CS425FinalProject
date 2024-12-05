# CS425FinalProject
## Team Members
Jered Fennell - Nicholas Merritt - Atharva Pargaonkar

## Link to demo

## File/Folders Manifest

- **`server.py`**:

- **`client.py`**:
    This file handles many things related to the client. Things like the client's list of channels that they are joined to. Clients have these key things:
    - **`nickname`**: This is assigned to the client after the nickname command. Each client is unique beforehand.

- **`channels.py`**:
    This file handles things related to the channels. It has a list of all the members that belong to it and a name. Channels have these key things:
    - **`name`**: This is assigned to the channel by the first client who joins it and is listed on the server.
    - **`clients`**: This is a list of all the clients who are members of the channel. When the last one leaves, the channel is removed.
    - **`thread`**

    
 ## Testing
 
### Manual Testing

A lot of testing was done manually. After making a change, we would start the server and the client, then connect to the default server on `localhost` at port `12345`.<br>
From there, we would test the adjusted commands, quit the session, and reconnect to verify persistence.<br>
Throughout this process, print statements helped confirm that the changes were functioning as intended.

 ## Reflections

 ### Nicholas Merritt

 ### Atharva Pargaonkar

 ### Jered Fennell

  