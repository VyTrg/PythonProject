from idlelib.macosx import hideTkConsole
from tkinter import *
from tkinter import messagebox
import sqlite3

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Member")
        self.resizable(False, False)

#Frame
    #Top Frames
        self.topFrame = Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=X)
    #Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg="#fcc324")
        self.bottomFrame.pack(fill=X)
    #Heading
        self.top_img = PhotoImage(file='../icons/add_member.png')
        top_img_label = Label(self.topFrame, image=self.top_img, bg='white')
        top_img_label.place(x=150, y=50)
        heading = Label(self.topFrame, text="Add Member", bg='white', fg='#003f8a', font='Arial 22 bold')
        heading.place(x=200, y=60)

    #Entries and labels
        #username
        self.label_username = Label(self.bottomFrame, text="Username: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_username.place(x=40, y=40)
        self.ent_username = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_username.insert(0, 'Please enter username')
        self.ent_username.place(x=150, y=45)
        #password
        self.label_password = Label(self.bottomFrame, text="Password: ",font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_password.place(x=40, y=80)
        self.ent_password = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_password.insert(0, 'Please enter password')
        self.ent_password.place(x=150, y=85)
        #phone
        self.label_phone = Label(self.bottomFrame, text="Phone: ", font='Arial 15 bold', bg='#fcc324', fg='white')
        self.label_phone.place(x=40, y=120)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Please enter phone number')
        self.ent_phone.place(x=150, y=125)
        #Button
        button = Button(self.bottomFrame, text='Add Member', command=self.addMember)
        button.place(x=200, y=160)

    def addMember(self):
        username = self.ent_username.get()
        password = self.ent_password.get()
        phone = self.ent_phone.get()

        if (username and password and phone != ''):
            try:
                conn = sqlite3.connect('library_management.db')
                cur = conn.cursor()
                query = "insert into 'login' (username, password, phone, status) values (?, ?, ?, ?)"
                cur.execute(query, (username, password, phone, True))
                conn.commit()
                messagebox.showinfo("Success", "Member has been added", icon='info')
                conn.close()
            except:
                messagebox.showerror("Error", "Member could not be added", icon='warning')
        else:
            messagebox.showerror("Error", "Field can't be empty", icon='warning')