import tkinter as tk
from tkinter import ttk


import account
from Library.library_management import BookCategory, Category, Author
from library_management import session, IssueReturnDetail, Book

import login

class ReaderWindow:
    def __init__(self, window, user):
        self.window = window
        self.window.title("Reader")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        self.user = user
        books = session.query(IssueReturnDetail, Book).join(Book).filter(IssueReturnDetail.username == self.user.username).all()


        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1000, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1000, relief=tk.RIDGE, bg="#e0f0f0", height=530)
        centerFrame.pack(side=tk.TOP)


        #combobox filter
        combobox_filter = ["All", "Issue", "Return"]
        self.combobox = ttk.Combobox(centerFrame, values=combobox_filter)
        self.combobox.current(0)
        self.combobox.place(x= 140, y=50, width=80, height=20)
        #book table
        column_name = ("Title", "ISBN", "Year", "Author", "Category", "Issue date", "Return date" ,"Status")
        self.tree = ttk.Treeview(centerFrame, columns=column_name, show='headings')
        for column in column_name:
            self.tree.heading(column, text=column, command= lambda c=column: self.sort_treeview(self.tree, column, False))
            self.tree.column(column, width=100, anchor=tk.CENTER)
        data = []
        for issue_return_detail, book in books:
            d = []
            categories = session.query(BookCategory, Category).join(Category).filter(book.book_id == BookCategory.category_id).all()
            cate = ""
            for book_cate, category in categories:
                cate = cate + category.category_name

            authors = session.query(Author).filter(book.book_id == Author.author_id).all()
            auth = ""

            for author in authors:
                auth = auth + author.name
            d.extend([book.title, book.isbn, book.year, auth, cate, issue_return_detail.date_issue, issue_return_detail.date_return, issue_return_detail.status])
            data.append(d)
            for item in data:
                self.tree.insert('', 'end', values=item)
        self.tree.place(x=10, y=80, width=980, height=400)
        # search book
        self.search_entry = tk.Entry(centerFrame)
        self.search_entry.place(x=10, y=50)

        self.search_button = tk.Button(centerFrame, text="Search", command=self.search_book())
        self.search_button.place(x=230, y=50, height=20)

        #logout
        self.buttonlogout = tk.Button(topFrame, text="Logout", compound=tk.RIGHT, font='arial 12 bold',
                                      command=self.logout)
        self.buttonlogout.pack(side=tk.RIGHT, padx=10)

        # account button
        self.iconaccount = tk.PhotoImage(file="assets/icons/user.png", height=50, width=50)
        self.buttonaccount = tk.Button(topFrame, text="Account", image=self.iconaccount, compound=tk.LEFT,
                                       font="arial 12", command=self.account)
        self.buttonaccount.pack(side=tk.LEFT, padx=10)

        # welcome user
        welcome_label = tk.Label(centerFrame, text="Welcome, " + str(self.user.name), font="arial 12", bg="#e0f0f0")
        welcome_label.place(x=10, y=10)

        # search book
        self.iconsearchbook = tk.PhotoImage(file="assets/icons/magnifying-glass.png", height=50, width=50)
        self.buttonsearchbook = tk.Button(topFrame, text="Search book", image=self.iconsearchbook, compound=tk.LEFT,
                                          font="arial 12")
        self.buttonsearchbook.pack(side=tk.LEFT, padx=10)

    def logout(self):
        self.window.destroy()
        login.run()

    def account(self):
        self.account = account.AccountSetting(self.user)

    # sort by column
    def sort_treeview(self, col, descending):
        data = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            self.tree.move(item, '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(self.tree, col, not descending))

    # search book
    def search_book(self):
        items = self.tree.get_children()
        search = self.search_entry.get().capitalize()
        for item in items:
            if search in (treeitem for treeitem in self.tree.item(item)['values'][0]):
                search_var = self.tree.item(item)['values']
                self.tree.delete(item)
                self.tree.insert("", 0, values=search_var)


def run(user):
    window = tk.Tk()
    ReaderWindow(window, user)
    window.mainloop()
