from server.serverGui import ServerGui
from server.server import Server
from threading import Thread
from tkinter import *
from main import Main
import socket
import os


loop = True
while loop:
    loop = False


    def warnWindow(arg, value):
        warnWin = Tk()
        warnWin.title("Invalid " + arg)
        warnWin.resizable(False, False)
        Label(warnWin, text = "Invalid " + arg + ": " + str(value)).pack()
        Button(warnWin, text = "Ok", command = warnWin.destroy).pack()
        warnWin.update_idletasks()
        warnWin.geometry("{}x{}+{}+{}".format(warnWin.winfo_width(), warnWin.winfo_height(), int(warnWin.winfo_screenwidth() / 2 - warnWin.winfo_width() / 2), int(warnWin.winfo_screenheight() / 2 - warnWin.winfo_height() / 2)))
        warnWin.mainloop()
    
    def startGame(event = None):
        global autoplay, loop, multiplayer
        for i in range(3):
            entry = entries[i]
            try:
                if float(entry.get()) != values[i]:
                    if i == 2:
                        values[i] = float(entry.get())
                    else:
                        values[i] = int(entry.get())
            except ValueError:
                warnWindow(options[i], str(entry.get()))
                return
        args = [*values, autoplay]
        for i in range(3):
            if args[i] <= 0:
                warnWindow(options[i], args[i])
                return
        mulVal = multiplayer.get()
        loop = True
        pos = "{}, {}".format(int(window.winfo_screenwidth() / 2 - 320), int(window.winfo_screenheight() / 2 - 240))
        window.destroy()
        noGame = False
        if mulVal:
            win = Tk()
            hostport = ["", ""]
            noGame = IntVar()
            noGame.set(1)
            serverThread = [None]
            stopServer = False
            def connect(new, hostport, serverThread):
                noGame.set(0)
                host = entry.get()
                port = spinbox.get()
                hostport[0] = host
                try:
                    int(port)
                except ValueError:
                    warnWindow("Port", port)
                    return
                hostport[1] = int(port)
                if new:
                    serverThread[0] = Thread(target=lambda: Server("", int(port)))
                    serverThread[0].start()
                win.destroy()
            win.title("Multiplayer")
            win.resizable(False, False)
            winFrame = Frame(win)
            winFrame.pack()
            Label(winFrame, text = "Host:").grid(row = 0, column = 0, sticky = E)
            entry = Entry(winFrame)
            entry.grid(row = 0, column = 1, sticky = W)
            Label(winFrame, text = "Port:").grid(row = 1, column = 0, sticky = E)
            spinbox = Spinbox(winFrame, from_ = 1, to = 9999)
            spinbox.grid(row = 1, column = 1, sticky = W)
            spinbox.delete(0, END)
            spinbox.insert(0, "8888")
            Button(win, text = "Connect", command = lambda: connect(0, hostport, serverThread)).pack(side = RIGHT)
            Button(win, text = "New Game", command = lambda: connect(1, hostport, serverThread)).pack(side = RIGHT)
            win.update_idletasks()
            win.geometry("{}x{}+{}+{}".format(win.winfo_width(), win.winfo_height(), int(win.winfo_screenwidth() / 2 - win.winfo_width() / 2), int(win.winfo_screenheight() / 2 - win.winfo_height() / 2)))
            win.mainloop()
            noGame = noGame.get()
            if not noGame:
                sgui = ServerGui(args[1:3])
                sgui.connect(*hostport)
                sgui.run()
                noGame = True
                if serverThread[0] != None:
                    serverThread[0].join()
        if not noGame:
            os.environ["SDL_VIDEO_WINDOW_POS"] = pos
            Main(*args)
        multiplayer.set(0)


    def setAutoplay():
        global autoplay
        autoplay = active.get()
    

    def terminate(event):
        window.destroy()
        loop = False
    

    def updateMultiplayer():
        if multiplayer.get():
            entries[0].configure(state = DISABLED)
        else:
            entries[0].configure(state = NORMAL)
    

    window = Tk()
    window.title("Snakefight")
    window.resizable(False, False)
    frame = Frame(window)
    frame.pack(expand = 1)
    options = ["Snakes", "Apples", "Speed"]
    values = [10, 5, 1.0]
    autoplay = 0
    entries = []
    for i in range(len(options)):
        label = Label(frame, text = options[i] + ":")
        label.grid(column = 0, row = i, sticky = E)
        if i == 2:
            from_ = 0.1
            increment = 0.1
        else:
            from_ = 1
            increment = 1
        entry = Spinbox(frame, from_ = from_, to = 1000, increment = increment)
        entry.grid(column = 1, row = i)
        entry.delete(0, END)
        entry.insert(0, str(values[i]))
        entries.append(entry)
    active = IntVar()
    active.set(0)
    Checkbutton(window, text = "Autoplay", variable = active, command = setAutoplay).pack(side = LEFT)
    Button(window, text = "Ok", command = startGame).pack(side = RIGHT)
    window.bind("<Return>", startGame)
    window.bind("<Escape>", terminate)
    multiplayer = IntVar()
    multiplayer.set(0)
    multiplayerOptions = [("Singleplayer", 0), ("Multiplayer", 1)]
    for option, value in multiplayerOptions:
        Radiobutton(window, text = option, variable = multiplayer, value = value, command = updateMultiplayer).pack(side=LEFT)
    window.update_idletasks()
    window.geometry("{}x{}+{}+{}".format(window.winfo_width(), window.winfo_height(), int(window.winfo_screenwidth() / 2 - window.winfo_width() / 2), int(window.winfo_screenheight() / 2 - window.winfo_height() / 2)))
    window.mainloop()
