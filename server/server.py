from server.errorWindow import ErrorWindow
from threading import Thread
import socket
import sys
import traceback
import json

class Server:
    def __init__(self, host, port):
        self.clients = []
        self.count = 0
        self.stop = False
        self.host = host
        self.port = port
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = []
        try:
            soc.bind((host, port))
        except:
            print("Bind failed. Error: ", sys.exc_info())
            ErrorWindow("Bind failed. Error: " + str(sys.exc_info()))
            sys.exit()
        soc.listen()
        while not self.stop:
            connection, address = soc.accept()
            if self.stop:
                break
            self.connections.append(connection)
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)
            try:
                Thread(target=self.clientThread, args=(connection, ip, port)).start()
            except Exception as error:
                print("Thread did not start.")
                ErrorWindow("Thread did not start: " + str(error))
                traceback.print_exc()
        soc.close()
    
    def setKey(self, index, key, value):
        try:
            self.clients[index][key] = value
        except KeyError:
            self.clients[index].setdefault(key)
            self.clients[index][key] = value

    def clientThread(self, connection, ip, port, maxBufferSize = 5120):
        self.clients.append({})
        client = self.clients[self.count]
        client["id"] = self.count
        self.count += 1
        isActive = True
        while isActive:
            clientInput = self.receiveInput(connection, maxBufferSize, lambda: client["id"])
            if clientInput == "exit" or self.stop:
                if client["id"] == 0:
                    self.stop = True
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((self.host, self.port))
                if self.stop:
                    connection.sendall("exit".encode("utf8"))
                connection.close()
                print("Connection " + ip + ":" + port + " closed")
                isActive = False
                self.count -= 1
                for otherClient in self.clients:
                    if otherClient["id"] > client["id"]:
                        otherClient["id"] -= 1
                del self.clients[client["id"]]
            elif clientInput == "start":
                for conn in self.connections:
                    conn.sendall(clientInput.encode("utf8"))
            else:
                connection.sendall(clientInput.encode("utf8"))

    def receiveInput(self, connection, maxBufferSize, index):
        clientInput = connection.recv(maxBufferSize)
        clientInputSize = sys.getsizeof(clientInput)
        if clientInputSize > maxBufferSize:
            print("The input size is greater than expected {}".format(clientInputSize))
        decodedInput = clientInput.decode("utf8").rstrip()
        result = self.processInput(decodedInput, index)
        return result

    def processInput(self, inputStr, index):
        if inputStr == "exit":
            return inputStr
        if inputStr == "start":
            return inputStr
        d = json.loads(inputStr)
        for key in d:
            self.setKey(index(), key, d[key])
        return chr(index()) + json.dumps(self.clients)
