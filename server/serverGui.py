from server.errorWindow import ErrorWindow
from random import randint, choice
from server.client import Client
from threading import Thread
from main import Main
from tkinter import *
import json
import time


class ServerGui(Tk):
    def __init__(self, args):
        super().__init__()
        self.title("Game")
        self.resizable(False, False)
        self.data = {"Color": [randint(0, 255), randint(0, 255), randint(0, 255)], "Ready": False}
        self.ready = False
        self.args = args
        self.optionsOpen = False
        self.destroyed = False
        self.finsished = False
    
    def destroy(self):
        self.client.close()
        self.destroyed = True
        return super().destroy()

    def randomExclude(self, randRange, exclude):
        randRange = list(randRange)
        for i in exclude:
            try:
                randRange.remove(i)
            except ValueError:
                pass
        return choice(randRange)

    def connect(self, host, port):
        self.client = Client(host, port, super().destroy, lambda: self.start(False))
        self.data["Speed"] = self.args[1]
        self.client.send(json.dumps(self.data))
        noR = []
        noG = []
        noB = []
        for client in self.client.clients:
            if client["Color"] == self.data["Color"]:
                noR.append(client["Color"][0])
                noG.append(client["Color"][1])
                noB.append(client["Color"][2])
        self.data["Color"] == [self.randomExclude(range(0, 255), noR), self.randomExclude(range(0, 255), noG), self.randomExclude(range(0, 255), noB)]
        self.client.send(json.dumps(self.data))

    def getPlayerData(self):
        names = []
        colors = []
        readys = []
        for client in self.client.clients:
            if client["id"] == self.client.id:
                names.append("Player " + str(client["id"]) + " (You)")
            else:
                names.append("Player " + str(client["id"]))
            colors.append(client["Color"])
            readys.append(client["Ready"])
        return names, colors, readys

    def fromRgb(self, rgb):
        rgb = tuple(rgb)
        return "#%02x%02x%02x" % rgb

    def getReady(self):
        self.ready = not self.ready
        self.data["Ready"] = self.ready
        self.refresh()
    
    def refresh(self):
        if self.client.id == 0:
            self.data["Speed"] = self.args[1]
        self.client.send(json.dumps(self.data))
        if self.client.clients == None:
            self.destroyed = True
            super().destroy()
            ErrorWindow("Server closed.")
            return
        try:
            self.args[1] = self.client.clients[0]["Speed"]
        except KeyError:
            pass
        pos = self.scrollbar.get()
        if len(pos) > 2:
            pos = (0.0, 0.0)
        self.listbox.delete(0, END)
        names, colors, readys = self.getPlayerData()
        for i in range(len(names)):
            if readys[i]:
                self.listbox.insert(END, names[i] + " (Ready)")
            else:
                self.listbox.insert(END, names[i])
            self.listbox.itemconfig(i, fg = self.fromRgb(colors[i]))
        self.listbox.yview_moveto(list(pos)[0])
        self.scrollbar.set(*pos)

    def start(self, send = True):
        if self.optionsOpen:
            ErrorWindow("You need to close the options window to start the game.", "Close it.")
        else:
            ready = True
            if send:
                for client in self.client.clients:
                    if not client["Ready"]:
                        ready = False
                        break
            if ready:
                if send:
                    self.client.send("start")
                else:
                    self.runRefresh = False
                    self.withdraw()
                    Main(1, *self.args, 0, self.client)
                    self.finsished = True
                    super().destroy()
            else:
                ErrorWindow("Wait until everyone is ready.", "Not so fast.")

    def buildGui(self):
        if self.client.id == 0:
            dataFrame = Frame(self)
            dataFrame.pack(expand = 1)
            Label(dataFrame, text = "Host:").grid(row = 0, column = 0)
            Label(dataFrame, text = "Port:").grid(row = 1, column = 0)
            entry = Entry(dataFrame)
            entry.grid(row = 0, column = 1)
            entry.insert(0, self.client.hostport[0])
            entry.config(state = "readonly")
            entry = Entry(dataFrame)
            entry.grid(row = 1, column = 1)
            entry.insert(0, str(self.client.hostport[1]))
            entry.config(state = "readonly")
        frame = Frame(self)
        frame.pack(expand = 1)
        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.listbox = Listbox(frame, yscrollcommand = self.scrollbar.set)
        names, colors, readys = self.getPlayerData()
        for i in range(len(names)):
            if readys[i]:
                self.listbox.insert(END, names[i] + " (Ready)")
            else:
                self.listbox.insert(END, names[i])
            self.listbox.itemconfig(i, fg = self.fromRgb(colors[i]))
        self.listbox.pack(side = LEFT, expand = 1)
        self.scrollbar.config(command = self.listbox.yview)
        if self.client.id == 0:
            Button(self, text = "Start", command = self.start).pack(side = RIGHT)
        Button(self, text = "Ready", command = self.getReady).pack(side = RIGHT)
        if self.client.id == 0:
            Button(self, text = "Options", command = lambda: Thread(target = self.optionsWindow).start()).pack(side = LEFT)

    def saveOptions(self, window):
        values = []
        for i in range(2):
            try:
                if i == 1:
                    values.append(float(self.entries[i].get()))
                else:
                    values.append(int(self.entries[i].get()))
                try:
                    if values[0] < 1 or values[1] < 0.1:
                        raise ValueError()
                except IndexError:
                    pass
            except ValueError:
                ErrorWindow("Invalid " + self.options[i] + ": " + str(self.entries[i].get()), "Invalid " + self.options[i])
                return
        for entry in self.entries:
            entry.destroy()
        for i in range(2):
            del self.entries[0]
        self.args = values
        self.data["Speed"] = self.args[1]
        self.client.send(json.dumps(self.data))
        window.destroy()

    def optionsWindow(self):
        self.optionsOpen = True
        window = Tk()
        window.title("Options")
        window.resizable(False, False)
        frame = Frame(window)
        frame.pack(expand = 1)
        self.options = ["Apples", "Speed"]
        values = self.args
        self.entries = []
        for i in range(len(self.options)):
            label = Label(frame, text = self.options[i] + ":")
            label.grid(column = 0, row = i, sticky = E)
            if i == 1:
                increment = 0.1
            else:
                increment = 1
            entry = Spinbox(frame, from_ = increment, to = 1000, increment = increment)
            entry.grid(column = 1, row = i)
            entry.delete(0, END)
            entry.insert(0, str(values[i]))
            self.entries.append(entry)
        Button(window, text = "Ok", command = lambda: self.saveOptions(window)).pack(side = RIGHT)
        window.bind("<Return>", lambda: self.saveOptions(window))
        window.bind("<Escape>", window.destroy)
        window.update_idletasks()
        window.geometry("{}x{}+{}+{}".format(window.winfo_width(), window.winfo_height(), int(window.winfo_screenwidth() / 2 - window.winfo_width() / 2), int(window.winfo_screenheight() / 2 - window.winfo_height() / 2)))
        window.mainloop()
        self.optionsOpen = False

    def refreshLoop(self):
        while self.runRefresh:
            if self.destroyed:
                break
            try:
                self.refresh()
            except (RuntimeError, TclError):
                break
            time.sleep(0.1)
    
    def run(self):
        self.buildGui()
        self.update_idletasks()
        self.geometry("{}x{}+{}+{}".format(self.winfo_width(), self.winfo_height(), int(self.winfo_screenwidth() / 2 - self.winfo_width() / 2), int(self.winfo_screenheight() / 2 - self.winfo_height() / 2)))
        self.runRefresh = True
        Thread(target = self.refreshLoop).start()
        self.mainloop()
        self.destroyed = True
        self.runRefresh = False
