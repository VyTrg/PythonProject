import tkinter as tk
from re import search
from tkinter import messagebox, Label, LabelFrame, Entry, Button, ttk

from sqlalchemy import values
from sqlalchemy.dialects.mssql.information_schema import columns

import login


class LibrianWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Librian")
        self.window.geometry("1350x750+350+200")

        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1350, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1350, height=680,  relief=tk.RIDGE, bg="#e0f0f0")
        centerFrame.pack(side=tk.TOP)

        centerLeftFrame = tk.Frame(centerFrame, width=900,height=700,  relief=tk.SUNKEN, bg="#f0f0f0", borderwidth=2)
        centerLeftFrame.pack(side=tk.LEFT)

        centerRightFrame = tk.Frame(centerFrame, width=450,height=700,  relief=tk.SUNKEN, bg="#e0f0f0", borderwidth=2)
        centerRightFrame.pack()

#Center Right Frame
        search_bar = LabelFrame(centerRightFrame, width=440, height=175, text='Search Box', bg='#9bc9ff')
        search_bar.pack(fill=tk.BOTH)
        self.search_bar = Label(search_bar, text='Search:', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.search_bar.grid(row=0, column=0, padx=20, pady=10)
        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=0, pady=10)
        self.btn_search = Button(search_bar, text='Search', font='arial 12 bold', bg='#fcc324', fg='white')
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)


        list_bar = LabelFrame(centerRightFrame, width=440, height=175, text='List Box', bg='#fcc324')
        list_bar.pack(fill=tk.BOTH)
        short_bar = Label(list_bar, text='Short by', font='times 16 bold', fg='#2488ff', bg='#fcc324')
        short_bar.grid(row=0, column=1)
        self.listChoice = tk.IntVar()
        radio_btn1 = tk.Radiobutton(list_bar, text='All Books', variable=self.listChoice, value=1, bg='#fcc324')
        radio_btn2 = tk.Radiobutton(list_bar, text='In Library', variable=self.listChoice, value=2, bg='#fcc324')
        radio_btn3 = tk.Radiobutton(list_bar, text='Borrowed Books', variable=self.listChoice, value=3, bg='#fcc324')
        radio_btn1.grid(row=1, column=0)
        radio_btn2.grid(row=1, column=1)
        radio_btn3.grid(row=1, column=2)
        list_btn = tk.Button(list_bar, text='List Books', font='arial 12', bg='#2488ff', fg='white')
        list_btn.grid(row=1, column=3, padx=40, pady=10)

        image_bar = tk.Frame(centerRightFrame, width=440, height=350)
        image_bar.pack(fill=tk.BOTH)
        self.title_right = LabelFrame(image_bar, text='Welcome to our Library!', font='arial 16 bold')
        self.title_right.grid(row=0)
        self.image_library = tk.PhotoImage(file='../icons/library.png')
        self.img_library = tk.Label(self.title_right, image=self.image_library)
        self.img_library.grid(row=0)

#Top Frame
        self.button_logout = tk.Button(topFrame, text="Log out", compound=tk.RIGHT, font='arial 12 bold', command=self.logout)
        self.button_logout.pack(side=tk.RIGHT, padx=10)

        self.icon_addbook = tk.PhotoImage(file='../icons/add_book.png')
        self.btn_addbook = tk.Button(topFrame, text="Add Book", image=self.icon_addbook, compound=tk.LEFT, font='arial 12 bold', command=self.add_book)
        self.btn_addbook.pack(side=tk.LEFT, padx=10)

        self.icon_addMember = tk.PhotoImage(file='../icons/add_member.png')
        self.btn_addMember = tk.Button(topFrame, text="Add Member", image=self.icon_addMember, compound=tk.LEFT,
                                     font='arial 12 bold', command=self.add_member)
        self.btn_addMember.pack(side=tk.LEFT, padx=10)

        self.icon_giveBook = tk.PhotoImage(file='../icons/give_book.png')
        self.btn_giveBook = tk.Button(topFrame, text="Give Book", image=self.icon_giveBook, compound=tk.LEFT,
                                       font='arial 12 bold', command=self.give_book)
        self.btn_giveBook.pack(side=tk.LEFT, padx=10)

#Center Left Frame
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.icon_management = tk.PhotoImage(file='../icons/management.png')
        self.icon_statistics = tk.PhotoImage(file='../icons/statistics.png')
        self.management = ttk.Frame(self.tabs)
        self.statistics = ttk.Frame(self.tabs)
        self.tabs.add(self.management, text='Library Management', image=self.icon_management, compound=tk.LEFT)
        self.tabs.add(self.statistics, text='Statistics', image=self.icon_statistics, compound=tk.LEFT)

    #Library Management
        #list books
        self.list_book = tk.Listbox(self.management, font='times 12 bold', width=40, height=30, bd=5)
        self.sb = ttk.Scrollbar(self.management, orient=tk.VERTICAL)
        self.list_book.grid(row=0, column=0, padx=(10,0), pady=10, sticky=tk.N)
        self.sb.config(command=self.list_book.yview)
        self.list_book.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E)

        #list details
        self.list_details = tk.Listbox(self.management, font='times 12 bold', width=80, height=30, bd=5)
        self.list_details.grid(row=0, column=1, padx=(10,0), pady=10, sticky=tk.N)

    #Statistics
        self.book_count = Label(self.statistics, text='Book Count', font='verdana 14 bold', pady=20)
        self.book_count.grid(row=0)
        self.member_count = Label(self.statistics, text='Member Count', font='verdana 14 bold', pady=20)
        self.member_count.grid(row=1, sticky=tk.W)
        self.taken_count = Label(self.statistics, text='Take Count', font='verdana 14 bold', pady=20)
        self.taken_count.grid(row=2, sticky=tk.W)

    def logout(self):
        self.window.destroy()
        login.page()

    def add_book(self):
        pass

    def add_member(self):
        pass

    def give_book(self):
        pass

def page():
    window = tk.Tk()
    LibrianWindow(window)
    window.mainloop()


if __name__ == '__main__':
    page()