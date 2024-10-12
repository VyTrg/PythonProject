from tkinter import *
from tkinter import messagebox
import sqlite3

class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False, False)

#Frame
    #Top Frames
        self.topFrame = Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=X)
    #Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg="#fcc324")
        self.bottomFrame.pack(fill=X)
    #Heading
        self.top_img = PhotoImage(file='../icons/add_book.png')
        top_img_label = Label(self.topFrame, image=self.top_img, bg='white')
        top_img_label.place(x=150, y=50)
        heading = Label(self.topFrame, text="Add Book", bg='white', fg='#003f8a', font='Arial 22 bold')
        heading.place(x=200, y=60)

    #Entries and labels
        #isbn
        self.label_isbn = Label(self.bottomFrame, text="ISBN: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_isbn.place(x=40, y=40)
        self.ent_isbn = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_isbn.insert(0, 'Please enter book ISBN')
        self.ent_isbn.place(x=150, y=45)
        #title
        self.label_title = Label(self.bottomFrame, text="Title: ",font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_title.place(x=40, y=80)
        self.ent_title = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_title.insert(0, 'Please enter book title')
        self.ent_title.place(x=150, y=85)
        #year
        self.label_year = Label(self.bottomFrame, text="Year: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_year.place(x=40, y=120)
        self.ent_year = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_year.insert(0, 'Please enter book year')
        self.ent_year.place(x=150, y=125)
        #quantity
        self.label_quantity = Label(self.bottomFrame, text="Quantity: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_quantity.place(x=40, y=160)
        self.ent_quantity = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_quantity.insert(0, 'Please enter book quantity')
        self.ent_quantity.place(x=150, y=165)
        #Button
        button = Button(self.bottomFrame, text='Add Book', command=self.addBook)
        button.place(x=200, y=200)

    def addBook(self):
        isbn = self.ent_isbn.get()
        title = self.ent_title.get()
        year = self.ent_year.get()
        quantity = self.ent_quantity.get()

        if (isbn and title and year and quantity != ''):
            try:
                conn = sqlite3.connect('library_management.db')
                cur = conn.cursor()
                query = "insert into 'book' (isbn, title, year, quantity) values (?, ?, ?, ?)"
                cur.execute(query, (isbn, title, year, quantity))
                conn.commit()
                messagebox.showinfo("Success", "Book has been added", icon='info')
                conn.close()
            except:
                messagebox.showerror("Error", "Book could not be added", icon='warning')
        else:
            messagebox.showerror("Error", "Field can't be empty", icon='warning')