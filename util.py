# Local address
localIP = "127.0.0.1"
localPort = 20001

# Options
bufferSize = 1024
timeout = 3
simulatePacketLoss = False

# Flags
flagFIN = 1
flagSYN = 2
flagPSH = 8
flagACK = 16


# Create a payload (write to bytes)
def makePayload(flags: int, seq: int, ack: int, data: str = None):
    bytesFlags = (flags).to_bytes(1, 'big')
    bytesSeq = (seq).to_bytes(2, 'big')
    bytesAck = (ack).to_bytes(2, 'big')

    payload = bytesFlags + bytesSeq + bytesAck

    if (data == None):
        return payload

    bytesData = data.encode()
    payload = bytesFlags + bytesSeq + bytesAck + bytesData
    return payload

# Parse data from a payload (read from bytes)
def readPayload(payload: bytes):
    flags = int.from_bytes(payload[:1], 'big')
    seqNumber = int.from_bytes(payload[1:3], 'big')
    ackNumber = int.from_bytes(payload[3:5], 'big')
    message = payload[5:].decode()
    return flags, seqNumber, ackNumber, message

# Check flags with ^
def checkFlags(flags, flagsToCheck):
    return flags ^ flagsToCheck == 0