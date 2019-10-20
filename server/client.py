from server.errorWindow import ErrorWindow
import json
import socket
import sys


class Client:
    def __init__(self, host = "127.0.0.1", port = 8888, errorFunc = None, startFunc = None):
        self.startFunc = startFunc
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
        except Exception as error:
            print("Connection error: ", error)
            if errorFunc != None:
                errorFunc()
            ErrorWindow("Connection error: " + str(error))
            exit()
        self.hostport = [list(self.socket.getsockname())[0], port]

    def send(self, data):
        self.socket.sendall(data.encode("utf8"))
        recv = self.socket.recv(5120).decode("utf8")
        if recv == "start":
            self.startFunc()
            return
        if not recv == "exit":
            self.id = ord(recv[0])
            text = ""
            for char in list(recv)[1:]:
                text += char
            try:
                self.clients = json.loads(text)
            except json.decoder.JSONDecodeError:
                pass
        else:
            self.clients = None
        return self.clients

    def close(self):
        self.socket.send("exit".encode("utf8"))
