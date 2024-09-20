import tkinter as tk
from re import search
from tkinter import messagebox, Label, LabelFrame, Entry, Button

from sqlalchemy.dialects.mssql.information_schema import columns

import login


class LibrianWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Librian")
        self.window.geometry("1100x600")

        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1000, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1000, relief=tk.RIDGE, bg="#e0f0f0", height=530)
        centerFrame.pack(side=tk.TOP)

        centerLeftFrame = tk.Frame(centerFrame, width=700, relief=tk.SUNKEN, bg="#f0f0f0", height=530, borderwidth=2)
        centerLeftFrame.pack(side=tk.LEFT)

        centerRightFrame = tk.Frame(centerFrame, width=300, relief=tk.SUNKEN, bg="#e0f0f0", height=530, borderwidth=2)
        centerRightFrame.pack()

        search_box = LabelFrame(centerRightFrame, width=300, height=100, text='Search Box', bg='#9bc9ff')
        search_box.pack(fill=tk.BOTH)
        self.search_bar = Label(search_box, text='Search:', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.search_bar.grid(row=0, column=0, padx=10, pady=10)
        self.ent_search = Entry(search_box, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=2, padx=0, pady=10)
        self.btn_search = Button(search_box, text='Search', font='arial 12 bold', bg='#fcc324', fg='white')
        self.btn_search.grid(row=0, column=4, padx=10, pady=10)

        list_bar = LabelFrame(centerRightFrame, width=700, height=150, text='List Box', bg='#fcc324')
        list_bar.pack(fill=tk.BOTH)

        self.buttonlogout = tk.Button(topFrame, text="Log out", compound=tk.RIGHT, font='arial 12 bold', command=self.logout)
        self.buttonlogout.pack(side=tk.RIGHT, padx=10)

        self.icon_addbook = tk.PhotoImage(file='../icons/add_book.png')
        self.btn_addbook = tk.Button(topFrame, text="Add Book", image=self.icon_addbook, compound=tk.LEFT, font='arial 12 bold')
        self.btn_addbook.pack(side=tk.LEFT, padx=10)

        self.icon_addmember = tk.PhotoImage(file='../icons/add_member.png')
        self.btn_addmember = tk.Button(topFrame, text="Add Member", image=self.icon_addmember, compound=tk.LEFT,
                                     font='arial 12 bold')
        self.btn_addmember.pack(side=tk.LEFT, padx=10)

        self.icon_givebook = tk.PhotoImage(file='../icons/give_book.png')
        self.btn_givebook = tk.Button(topFrame, text="Give Book", image=self.icon_givebook, compound=tk.LEFT,
                                       font='arial 12 bold')
        self.btn_givebook.pack(side=tk.LEFT, padx=10)

    def logout(self):
        self.window.destroy()
        login.page()

    def addbook(self):
        self.window.destroy()

    def addmember(self):
        self.window.destroy()

def page():
    window = tk.Tk()
    LibrianWindow(window)
    window.mainloop()


if __name__ == '__main__':
    page()