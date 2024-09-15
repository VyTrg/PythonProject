import tkinter as tk
from tkinter import messagebox, Label

import login

class ReaderWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Reader")
        self.window.geometry("1000x600")

        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1000, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1000, relief=tk.RIDGE, bg="#e0f0f0", height=530)
        centerFrame.pack(side=tk.TOP)

        # self.iconlogout = tk.PhotoImage(file="assets/icons/logout.png")
        self.buttonlogout = tk.Button(topFrame, text="Logout", compound=tk.RIGHT, font='arial 12 bold', command=self.logout)
        self.buttonlogout.pack(side=tk.RIGHT, padx=10)

    def logout(self):
        self.window.destroy()
        login.page()


def page():
    window = tk.Tk()
    ReaderWindow(window)
    window.mainloop()

if __name__ == '__main__':
    page()