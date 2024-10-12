from tkinter import *
from tkinter import messagebox, Label, ttk, Button

import tkinter as tk
from tkinter.ttk import Combobox

import sqlite3

conn = sqlite3.connect('library_management.db')
cur = conn.cursor()

class RequestBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Request Book")
        self.resizable(False, False)

        query = "select * from book as b inner join book_request as r on b.book_id = r.book_id where r.issue_return = false"
        result = cur.execute(query).fetchall()
        request_list = []
        for re in result:
            request_list.append(str(re[0]) + ' - ' + re[2] + ' - ' + re[8])

#Frame
    #Top Frames
        self.topFrame = Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=X)
    #Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg="#fcc324")
        self.bottomFrame.pack(fill=X)
    #Heading
        self.top_img = PhotoImage(file='../icons/book_request.png')
        top_img_label = Label(self.topFrame, image=self.top_img, bg='white')
        top_img_label.place(x=150, y=50)
        heading = Label(self.topFrame, text="Request Book", bg='white', fg='#003f8a', font='Arial 22 bold')
        heading.place(x=200, y=60)

    #Labels
        self.label_request = Label(self.bottomFrame, text='Request', font='verdana 14 bold', pady=20,  bg='#fcc324')
        self.label_request.place(x=40, y=15)
        self.combobox_request = Combobox(self.bottomFrame, width=40)
        self.combobox_request['values'] = request_list
        self.combobox_request.place(x=150, y=40)
    #Button
        button = Button(self.bottomFrame, text='Accept', command=self.acceptRequest)
        button.place(x=450, y=40)

    def acceptRequest(self):
        value = self.combobox_request.get()
        book_id = int(value.split('-')[0])
        username = value.split('-')[2].strip()
        if (book_id and username != ''):
            try:
                query = "update book_request set issue_return = TRUE where book_id = ? and username = ?"
                cur.execute(query, (book_id, username))
                conn.commit()
                messagebox.showinfo("Notifications", "Book Request Accepted", icon='info')
                conn.close()
            except:
                messagebox.showinfo("Error", "Something went wrong", icon='error')
        else:
            messagebox.showinfo("Error", "Please enter a valid book name or member name", icon='warning')