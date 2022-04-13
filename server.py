import random
import socket
import sys
import util

serverSeqNumber = 1000
startSync = False
startShutdown = False
connectionEstablished = False

ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
ServerSocket.bind((util.localIP, util.localPort))
print("RUDP server up and running!\n")

while 1:
    clientResponse = ServerSocket.recvfrom(util.bufferSize)
    payload = clientResponse[0]
    address = clientResponse[1]

    clientFlags, clientSeqNumber, clientAckNumber, clientMessage = util.readPayload(payload)

    # Syn handshake
    if util.checkFlags(clientFlags, util.flagSYN):
        startSync = True
        print(f"Client {address} wants to synchronize sequence number...")

        serverSeqNumber = 1000
        serverAckNumber = clientSeqNumber + 1

        serverPayload = util.makePayload((util.flagACK | util.flagSYN), serverSeqNumber, serverAckNumber)
        ServerSocket.sendto(serverPayload, address)
    
    # Ack handshake
    elif util.checkFlags(clientFlags, util.flagACK) and startSync:
        startSync = False
        print(f"Syncronization successful with client {address}!\n")
        connectionEstablished = True

    # Data transfer
    elif util.checkFlags(clientFlags, util.flagPSH) and connectionEstablished:
        print(f"Message from client {address} : '{clientMessage}'\n")

        if util.simulatePacketLoss:
        # Simulate packet loss 50% chance
            packetLoss = random.getrandbits(1)
        else:
            packetLoss = 1
        
        if packetLoss:
            serverPayload = util.makePayload(util.flagACK, serverSeqNumber, clientSeqNumber + sys.getsizeof(clientMessage))
            ServerSocket.sendto(serverPayload, address)
    
    # Fin shutdown
    elif util.checkFlags(clientFlags, util.flagFIN):
        print(f"Client {address} wants to close the connection...")
        startShutdown = True

        serverPayload = util.makePayload(util.flagACK, serverSeqNumber, serverAckNumber)
        ServerSocket.sendto(serverPayload, address)

        serverPayload = util.makePayload(util.flagFIN, serverSeqNumber, serverAckNumber)
        ServerSocket.sendto(serverPayload, address)

    # Ack shutdown
    elif util.checkFlags(clientFlags, util.flagACK) and startShutdown:
        startShutdown = False
        connectionEstablished = False
        print("Connection closed, goodbye client!\n")

    else:
        print(f'Client {address} tried sending some payload, but probably the connection was not properly established.\n')
