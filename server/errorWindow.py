from tkinter import *


class ErrorWindow(Tk):
    def __init__(self, text, title = "Error"):
        super().__init__()
        self.title(title)
        Label(self, text = text).pack()
        Button(self, text = "Ok", command = self.destroy).pack()
        self.update_idletasks()
        self.geometry("{}x{}+{}+{}".format(self.winfo_width(), self.winfo_height(), int(self.winfo_screenwidth() / 2 - self.winfo_width() / 2), int(self.winfo_screenheight() / 2 - self.winfo_height() / 2)))
        self.mainloop()
