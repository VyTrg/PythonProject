import tkinter as tk
from tkinter import messagebox, Label, LabelFrame, Entry, Button, ttk


import login
import add_book, add_member, give_book, request_book, edit_book

import sqlite3

conn = sqlite3.connect('library_management.db')
cur = conn.cursor()

class LibrianWindow:
    def __init__(self, window):
        self.edit_book = None
        self.window = window
        self.window.title("Librian")
        self.window.geometry("1350x750+350+200")

        def displayStatistic(evt):
            count_book = cur.execute("SELECT COUNT(book_id) FROM book").fetchall()
            count_member = cur.execute("SELECT COUNT(username) FROM login where username like '%reader%';").fetchall()
            taken_book = cur.execute("select count(book_id) from issue_return_detail").fetchall()
            self.label_book_count.config(text='Total Books: ' + str(count_book[0][0]) + ' in library')
            self.label_member_count.config(text='Total Members: ' + str(count_member[0][0]))
            self.label_taken_count.config(text='Taken Books: ' + str(taken_book[0][0]))
            displayBooks(self)

        def displayBooks(self):
            books = cur.execute('SELECT * FROM book').fetchall()
            count = 0
            self.list_book.delete(0, 'end')
            for book in books:
                self.list_book.insert(count, str(book[0])+' - '+book[2])
                count += 1

            def bookInfo(evt):
                value = str(self.list_book.get(self.list_book.curselection()))
                id = value.split('-')[0]
                book = cur.execute('SELECT * FROM book WHERE book_id=?', (id,))
                book_info = book.fetchall()
                self.list_details.delete(0, 'end')
                self.list_details.insert(0, 'ISBN: ' + book_info[0][1])
                self.list_details.insert(1, 'Title: ' + book_info[0][2])
                self.list_details.insert(2, 'Year: ' + str(book_info[0][3]))
                self.list_details.insert(3, 'Quantity: ' + str(book_info[0][4]))
                if str(book_info[0][5]) != 'None':
                    self.list_details.insert(4, 'IMG: ' + book_info[0][5])

            def doubleClick(evt):
                global given_id
                value = str(self.list_book.get(self.list_book.curselection()))
                given_id = value.split('-')[0]
                given_book = GiveBook()

            self.list_book.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatistic)
            #self.tabs.bind('<ButtonRelease-1>', displayBooks)
            self.list_book.bind('<Double-Button-1>', doubleClick)

#Frame
        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1350, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1350, height=680,  relief=tk.RIDGE, bg="#e0f0f0")
        centerFrame.pack(side=tk.TOP)

        centerLeftFrame = tk.Frame(centerFrame, width=900,height=680,  relief=tk.SUNKEN, bg="#f0f0f0", borderwidth=2)
        centerLeftFrame.pack(side=tk.LEFT)

        centerRightFrame = tk.Frame(centerFrame, width=450,height=680,  relief=tk.SUNKEN, bg="#e0f0f0", borderwidth=2)
        centerRightFrame.pack()

#Center Right Frame
        search_bar = LabelFrame(centerRightFrame, width=440, height=175, text='Search Box', bg='#9bc9ff')
        search_bar.pack(fill=tk.BOTH)
        self.search_bar = Label(search_bar, text='Search:', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.search_bar.grid(row=0, column=0, padx=20, pady=10)
        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=0, pady=10)
        self.btn_search = Button(search_bar, text='Search', font='arial 12 bold', bg='#fcc324', fg='white', command=self.search_book)
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
        list_btn = tk.Button(list_bar, text='Short', font='arial 12', bg='#2488ff', fg='white', command=self.list_books)
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

        self.button_edit = tk.Button(topFrame, text="Edit Book", compound=tk.RIGHT, font='arial 12 bold',
                                     command=self.open_edit_book)  # Updated command
        self.button_edit.pack(side=tk.RIGHT, padx=10)


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


         # command = self.edit_book

    #book request
        self.book_request = tk.PhotoImage(file='../icons/book_request.png')
        self.btn_bookRequest = tk.Button(topFrame, text="Request Book", image=self.book_request, font='arial 12 bold', compound=tk.LEFT, command=self.request_book)
        self.btn_bookRequest.pack(side=tk.LEFT, padx=10)

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
        self.sb = tk.Scrollbar(self.management, orient=tk.VERTICAL)
        self.list_book.grid(row=0, column=0, padx=(10,0), pady=10, sticky=tk.N)
        self.sb.config(command=self.list_book.yview)
        self.list_book.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E)

        #list details
        self.list_details = tk.Listbox(self.management, font='times 12 bold', width=60, height=30, bd=5)
        self.list_details.grid(row=0, column=1, padx=(10,0), pady=10, sticky=tk.N)

    #Statistics
        self.label_book_count = Label(self.statistics, font='verdana 14 bold', pady=20)
        self.label_book_count.grid(row=0,sticky=tk.W)
        self.label_member_count = Label(self.statistics, font='verdana 14 bold', pady=20)
        self.label_member_count.grid(row=1, sticky=tk.W)
        self.label_taken_count = Label(self.statistics, font='verdana 14 bold', pady=20)
        self.label_taken_count.grid(row=2, sticky=tk.W)

    #functions
        displayBooks(self)
        displayStatistic(self)

    def logout(self):
        self.window.destroy()
        login.run()

    def open_edit_book(self):
        self.edit_book = edit_book.EditBook()  # Create an instance of EditBook

    def list_books(self):
        value = self.listChoice.get()
        if value == 1: #sách trong thư viện
            all_books = cur.execute("SELECT * FROM book").fetchall()
            self.list_book.delete(0, tk.END)
            count = 0
            for book in all_books:
                self.list_book.insert(count, str(book[0])+' - '+book[2])
                count += 1
        elif value == 2: #sách chưa mượn
            book_in_library = cur.execute("SELECT * FROM book as b LEFT JOIN issue_return_detail as i on b.book_id = i.book_id where i.book_id is null;").fetchall()
            self.list_book.delete(0, tk.END)
            count = 0
            for book in book_in_library:
                self.list_book.insert(count, str(book[0])+' - '+book[2])
                count += 1
        else: #sách đã mượn
            takens_book = cur.execute("SELECT * FROM book as b inner join issue_return_detail as i on b.book_id = i.book_id").fetchall()
            self.list_book.delete(0, tk.END)
            count = 0
            for book in takens_book:
                self.list_book.insert(count, str(book[0]) + ' - ' + book[2])
                count += 1

    def search_book(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM book WHERE title LIKE ?;", ('%'+value+'%',)).fetchall()
        self.list_book.delete(0, tk.END)
        count=0
        for book in search:
            self.list_book.insert(count, str(book[0]) + " - " + book[2])
            count += 1

    def add_book(self):
        add = add_book.AddBook()

    def add_member(self):
        add = add_member.AddMember()

    def give_book(self):
        give = give_book.GiveBook()

    def request_book(self):
        num_request = cur.execute("select count(issue_return) from book_request where issue_return = FALSE").fetchone()
        value = num_request[0]
        if value == 0:
            messagebox.showinfo("Notifications", "You have no book request")
        else:
            request = request_book.RequestBook()

def run():
    window = tk.Tk()
    LibrianWindow(window)
    window.mainloop()

class GiveBook(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False, False)
        global given_id
        self.book_id = int(given_id)
        query = "select * from book"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + " - " + book[2])

        query1 = "select * from login where username like '%reader%'"
        members = cur.execute(query1).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]))

# Frame
    # Top Frames
        self.topFrame = tk.Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=tk.X)
        # Bottom Frame
        self.bottomFrame = tk.Frame(self, height=600, bg="#fcc324")
        self.bottomFrame.pack(fill=tk.X)
    # Heading
        self.top_img = tk.PhotoImage(file='../icons/give_book.png')
        top_img_label = Label(self.topFrame, image=self.top_img, bg='white')
        top_img_label.place(x=150, y=50)
        heading = Label(self.topFrame, text="Lend Book", bg='white', fg='#003f8a', font='Arial 22 bold')
        heading.place(x=200, y=60)

    # Entries and labels
        # book
        self.book_name = tk.StringVar()
        self.label_book = Label(self.bottomFrame, text="Book: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_book.place(x=40, y=40)
        self.combobox_book_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combobox_book_name['values'] = book_list
        self.combobox_book_name.current(self.book_id - 1)
        self.combobox_book_name.place(x=150, y=45)

        # member
        self.username = tk.StringVar()
        self.label_member = Label(self.bottomFrame, text="Member: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_member.place(x=40, y=80)
        self.combobox_member = ttk.Combobox(self.bottomFrame, textvariable=self.username)
        self.combobox_member['values'] = member_list
        self.combobox_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text='Lend Book', command=self.lendBook)
        button.place(x=200, y=120)

    def lendBook(self):
        book_name = self.book_name.get()
        username = self.username.get()
        book_id = book_name.split('-')[0]
        if (book_name and username != ""):
            try:
                query = "insert into 'book_request' (book_id, username, issue_return) values (?, ?, ?)"
                cur.execute(query, (book_id, username, False))
                conn.commit()
                messagebox.showinfo("Success", "Request has been sent", icon='info')
            except Exception as e:
                print(e)
                messagebox.showinfo("Error", "Something went wrong", icon='error')
        else:
            messagebox.showinfo("Error", "Please enter a valid book name or member name", icon='warning')

if __name__ == '__main__':
    window = tk.Tk()
    LibrianWindow(window)
    window.mainloop()