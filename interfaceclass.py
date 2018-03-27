"""GUI using optimal object-oriented programming."""

from tkinter import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("lowkeyluke's Blackjack")
        quitbutton = Button(text="Quit", command=self.client_exit)
        quitbutton.place(x=0, y=0)

    def client_exit(self):
        exit()


root = Tk()
root.geometry("400x400")
window = Window(root)

window.mainloop()