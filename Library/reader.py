import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL, VERTICAL

import account
from library_management import BookCategory, Category, Author
from library_management import session, IssueReturnDetail, Book

import login


def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + " " + word) <= width:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

class ReaderWindow:
    def __init__(self, window, user):
        self.window = window
        self.window.title("Reader")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        self.user = user
        issuereturn = session.query(IssueReturnDetail).filter(IssueReturnDetail.username == self.user.username).all()
        self.books = []
        for i in issuereturn:
            b = session.query(Book).filter(Book.book_id == i.book_id).first()
            book = {
                'title' : b.title,
                'isbn' : b.isbn,
                'year' : b.year,
                'issue_date': i.date_issue,
                'return_date': i.date_return,
                'status': i.status,
                'image' : b.image
            }
            cate_book = session.query(BookCategory).filter(BookCategory.book_id == b.book_id).all()
            cate = []
            for j in cate_book:
                k = session.query(Category).filter(Category.category_id == j.category_id).first()
                cate.append(k.category_name)
            book['category'] = ','.join(cate)
            auth = []
            authors = session.query(Author).filter(Author.author_id == i.book_id).all()
            for j in authors:
                auth.append(j.name)
            book['author'] = ','.join(auth)
            self.books.append(book)

        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1000, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1000, relief=tk.RIDGE, bg="#e0f0f0", height=530)
        centerFrame.pack(side=tk.TOP)
        #combobox filter
        combobox_filter = ["All", "Issued", "Returned"]
        self.combobox = ttk.Combobox(centerFrame, values=combobox_filter)
        self.combobox.current(0)
        self.combobox.place(x= 140, y=50, width=80, height=20)

        #book table
        column_name = ("Title","Status")
        self.tree = ttk.Treeview(centerFrame, columns=column_name, show='headings')
        for column in column_name:
            self.tree.heading(column, text=column, command= lambda c=column: self.sort_treeview(self.tree, column, False))
            self.tree.column(column, width=100, anchor=tk.CENTER)
        data = []
        for book in self.books:
            d = []
            d.extend([book['title'], book['status']])
            data.append(d)
        for item in data:
            self.tree.insert('', 'end',values=item)
        self.tree.place(x=10, y=80, width=300, height=400)
        self.tree.bind('<Double-1>', self.clicker)
        self.scrollbar_tree = ttk.Scrollbar(self.tree, orient=VERTICAL)
        self.scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar_tree.set)
        self.scrollbar_tree.config(command=self.tree.yview)
        # search book
        self.search_entry = tk.Entry(centerFrame)
        self.search_entry.place(x=10, y=50)

        self.search_button = tk.Button(centerFrame, text="Search", command=self.search_book)
        self.search_button.place(x=230, y=50, height=20)

        #logout
        self.buttonlogout = tk.Button(topFrame, text="Logout", compound=tk.RIGHT, font='arial 12 bold',
                                      command=self.logout)
        self.buttonlogout.pack(side=tk.RIGHT, padx=10)

        # account button
        self.iconaccount = tk.PhotoImage(file="assets//icons//user.png", height=50, width=50)
        self.buttonaccount = tk.Button(topFrame, text="Account", image=self.iconaccount, compound=tk.LEFT,
                                       font="arial 12", command=self.account)
        self.buttonaccount.pack(side=tk.LEFT, padx=10)

        # welcome user
        welcome_label = tk.Label(centerFrame, text="Welcome, " + str(self.user.name), font="arial 12", bg="#e0f0f0")
        welcome_label.place(x=10, y=10)

        # search book
        self.iconsearchbook = tk.PhotoImage(file="assets//icons//magnifying-glass.png", height=50, width=50)
        self.buttonsearchbook = tk.Button(topFrame, text="Search book", image=self.iconsearchbook, compound=tk.LEFT,
                                          font="arial 12")
        self.buttonsearchbook.pack(side=tk.LEFT, padx=10)

        #display whole book information
        self.list_book = tk.Listbox(centerFrame, selectmode=tk.SINGLE)
        self.list_book.place(x= 350, y= 80,  width=300, height=400)
        self.scrollbar_listboox = tk.Scrollbar(self.list_book, orient=HORIZONTAL)
        self.scrollbar_listboox.pack(side=tk.BOTTOM, fill=tk.X)
        self.list_book.config(xscrollcommand=self.scrollbar_listboox.set)
        self.scrollbar_listboox.config(command=self.list_book.xview)
        #book image
        self.book_image = tk.PhotoImage(file="", height=300, width=250)
        self.label = tk.Label(centerFrame, image=self.book_image, bg="#e0f0f0")
        self.label.place(x=700, y=80)
        #combobox filter
        def option_selected(event):
            select_option = self.combobox.get()
            if select_option != "All":
                items = self.tree.get_children()
                for item in items:
                    self.tree.delete(item)
                    if self.tree.item(item)['values'][1] == select_option:
                        filter_value = self.tree.item(item)['values']
                        self.tree.insert("", 0, values=filter_value)

            else:
                items = self.tree.get_children()
                for item in items:
                    self.tree.insert("", 0, values=item)


        self.combobox.bind('<<ComboboxSelected>>', option_selected)

    def clicker(self, event):
        selected = self.tree.selection()
        item = self.tree.item(selected, "values")
        for book in self.books:
            if item[0] == book['title']:
                self.list_book.delete(0, tk.END)
                self.list_book.insert(tk.END, "Title :" + book['title'])
                self.list_book.insert(tk.END, "ISBN :" + book['isbn'])
                self.list_book.insert(tk.END, "Author :" + book['author'])
                self.list_book.insert(tk.END, "Category :" + book['category'])
                self.list_book.insert(tk.END, "Year :" + str(book['year']))
                self.list_book.insert(tk.END, "Issue date :" + str(book['issue_date']))
                self.list_book.insert(tk.END, "Return date :" + str(book['return_date']))
                self.list_book.insert(tk.END, "Status :" + str(book['status']))
                self.book_image.blank()
                self.book_image.config(file="E:\\Year_3\\Semester_1_0_7\\python_project\\Library\\assets\\book_image\\" + book['image'])

    def logout(self):
        self.window.destroy()
        login.run()

    def account(self):
        self.account = account.AccountSetting(self.user)



    # search book
    def search_book(self):
        items = self.tree.get_children()
        search = self.search_entry.get().capitalize()
        for item in items:
            if search in (treeitem for treeitem in self.tree.item(item)['values'][0]):
                search_var = self.tree.item(item)['values']
                self.tree.delete(item)
                self.tree.insert("", 0, values=search_var)

    # sort by column
    def sort_treeview(self, tree, col, descending):
        data = [(tree.set(item, col), item) for item in tree.get_children()]
        data.sort(reverse=descending)
        for index, (val, item) in enumerate(data):
            tree.move(item, '', index)
            tree.heading(col, command=lambda: self.sort_treeview(tree, col, not descending))



def run(user):
    window = tk.Tk()
    ReaderWindow(window, user)
    window.mainloop()
