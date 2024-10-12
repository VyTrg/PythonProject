import tkinter as tk
from tkinter import messagebox, Label, LabelFrame, Entry, Button, ttk
import sqlite3

conn = sqlite3.connect('library_management.db')
cur = conn.cursor()

class GiveBook(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False, False)

        query = "SELECT * FROM book as b LEFT JOIN issue_return_detail as i on b.book_id = i.book_id where i.book_id is null;"
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
                conn.close()
            except:
                messagebox.showinfo("Error", "Something went wrong", icon='error')
        else:
            messagebox.showinfo("Error", "Please enter a valid book name or member name", icon='warning')
