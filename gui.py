from tkinter import *
from main import Main
import os


loop = True
while loop:
    loop = False

    
    def startGame():
        global autoplay, loop
        for i in range(3):
            entry = entries[i]
            if float(entry.get()) != values[i]:
                if i == 2:
                    values[i] = float(entry.get())
                else:
                    values[i] = int(entry.get())
        args = [*values, autoplay]
        for i in range(3):
            if args[i] <= 0:
                warnWin = Tk()
                warnWin.title("Invalid " + str(options[i]))
                warnWin.resizable(False, False)
                Label(warnWin, text = "Invalid " + str(options[i]) + ": " + str(args[i])).pack()
                Button(warnWin, text = "Ok", command = warnWin.destroy).pack()
                warnWin.update_idletasks()
                warnWin.geometry("{}x{}+{}+{}".format(warnWin.winfo_width(), warnWin.winfo_height(), int(window.winfo_screenwidth() / 2 - warnWin.winfo_width() / 2), int(window.winfo_screenheight() / 2 - warnWin.winfo_height() / 2)))
                warnWin.mainloop()
                return
        loop = True
        os.environ["SDL_VIDEO_WINDOW_POS"] = "{}, {}".format(int(window.winfo_screenwidth() / 2 - 320), int(window.winfo_screenheight() / 2 - 240))
        window.destroy()
        Main(*args)


    def setAutoplay():
        global autoplay
        autoplay = active.get()


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
    checkbox = Checkbutton(window, text = "Autoplay", variable = active, command = setAutoplay)
    checkbox.pack(side = LEFT)
    button = Button(window, text = "Ok", command = startGame)
    button.pack(side = RIGHT)
    window.update_idletasks()
    window.geometry("{}x{}+{}+{}".format(window.winfo_width(), window.winfo_height(), int(window.winfo_screenwidth() / 2 - window.winfo_width() / 2), int(window.winfo_screenheight() / 2 - window.winfo_height() / 2)))
    window.mainloop()
