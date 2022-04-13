# RUDP Protocol
Built a server and client for the Reliable UDP communications protocol. Added parts of the TCP protocol such as flags, 3-way handhsake, SEQ, ACK numbers on top of the standard UDP protocol.
It is less complex than TCP, but realiable unlike UDP.

## Prerequisites
Download and install [Python](https://www.python.org/downloads/).

## Installation
[Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or [download](https://www.itprotoday.com/development-techniques-and-management/how-do-i-download-files-github) the files.
Place everything in a folder.

## Usage
Double-click the start.bat file to start the server.

Alternatively, it can be started using a command prompt command run in the main directory of the project as such:

```bash
python server.py
```

Likewise, you can now run the client using:

```bash
python client.py
```

Congrats, now you can send data between the user and the server!

By default, the server will run on IP 127.0.0.1 and port 20001. These can be modified in the util.py file, along with some other settings.

To send different data to the server you can modify the client's main function between the startup and shutdown calls.
