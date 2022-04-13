import socket
import sys
import util

# Initiation settings
clientSeqNumber = 1
serverAddressPort = (util.localIP, util.localPort)
clientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
clientSocket.settimeout(util.timeout)

# 3 way handshake to initiate the connection
def startup():
    # Send package with SYN flag
    print("Starting client...")
    clientPayload = util.makePayload(util.flagSYN, clientSeqNumber, 0)
    clientSocket.sendto(clientPayload, serverAddressPort)

    # Get server answer and check if it has both the SYN and ACK flags
    serverResponse = clientSocket.recvfrom(util.bufferSize)
    payload = serverResponse[0]
    serverFlags, serverSeqNumber, serverAckNumber, serverMessage = util.readPayload(payload)

    # If it does, and the ACK number sent back is good the client sends a package with the ACK flag
    if util.checkFlags(serverFlags, util.flagSYN | util.flagACK) and serverAckNumber == clientSeqNumber + 1:
        clientPayload = util.makePayload(util.flagACK, serverAckNumber + 1, serverSeqNumber + 1)
        clientSocket.sendto(clientPayload, serverAddressPort)
        print("Sequence number syncronization succeded.")

    else:
        print("Sequence number syncronization failed.")
        exit()

    print("Connection established.")

# Send a payload with data to the server
def sendData(text: str, noTries: int = 0):
    # Send some data using the PSH flag
    print("Sending some data...")
    clientPayload = util.makePayload(util.flagPSH, clientSeqNumber, 0, text)
    clientSocket.sendto(clientPayload, serverAddressPort)
    
    try:
        # Get server answer and check if it has the ACK flag
        serverResponse = clientSocket.recvfrom(util.bufferSize)
        payload = serverResponse[0]
        serverFlags, serverSeqNumber, serverAckNumber, serverMessage = util.readPayload(payload)

    except socket.timeout:
        if noTries == 3:
            print("Data transfer timed out 3 times, try again later.")
            return
        print("Data transfer timed out, trying again...")
        sendData(text, noTries + 1)
        return
    
    # If it does, the data was succesfully sent and received
    if util.checkFlags(serverFlags, util.flagACK) and clientSeqNumber + sys.getsizeof(text) == serverAckNumber:
        print("The data was succesfully sent.")
    else:
        print("Data transfer failed.")
    
# Close the connection
def shutdown():
    # Send a package with the FIN flag
    print("Closing connection...")
    clientPayload = util.makePayload(util.flagFIN, clientSeqNumber, 0)
    clientSocket.sendto(clientPayload, serverAddressPort)

    # Get server answer and check if it has the ACK flag
    serverResponse = clientSocket.recvfrom(util.bufferSize)
    payload = serverResponse[0]
    serverFlags, serverSeqNumber, serverAckNumber, serverMessage = util.readPayload(payload)

    # If it does, wait check if the following package sent from the server has the FIN flag
    if util.checkFlags(serverFlags, util.flagACK):
        serverResponse = clientSocket.recvfrom(util.bufferSize)
        payload = serverResponse[0]
        serverFlags, serverSeqNumber, serverAckNumber, serverMessage = util.readPayload(payload)

        # If it does, send a package containing the ACK flag to the server, and the connection was succesfully closed
        if util.checkFlags(serverFlags, util.flagFIN):
            print("Connection succesfully closed.")
            clientPayload = util.makePayload(util.flagACK, clientSeqNumber, 0)
            clientSocket.sendto(clientPayload, serverAddressPort)
            print("Closing client...")
            exit()
        
        else:
            print("Server aknowledged, but didn't close the connection.")
            return

    else:
        print("Connection closure failed.")
        return

if __name__ == "__main__":
    # Startup
    startup()

    # Send some data
    sendData("Hello world!")
    sendData("Packet 1")

    # Shutdown
    shutdown()
