import tkinter as tk

from tkinter import messagebox as mb

from sqlalchemy import update
from sqlalchemy.orm import Session, sessionmaker

from library_management import Login, engine



class AccountSetting(tk.Toplevel):
    def __init__(self, user):
        tk.Toplevel.__init__(self)
        self.title("Account Setting")
        self.geometry("650x300")
        self.resizable(False, False)

        self.user = user

        #top frame
        self.topFrame = tk.Frame(self, height=100, bg='white')
        self.topFrame.pack(fill=tk.X)

        #bottom frame
        self.bottomFrame = tk.Frame(self, height=400, bg='#e0f0f0')
        self.bottomFrame.pack(fill=tk.X)

        #top image
        self.topImage = tk.PhotoImage(file='assets/icons/accountSetting.png')
        topImageLabel = tk.Label(self.topFrame, image=self.topImage, bg='white')
        topImageLabel.place(x=120,y=10)
        heading = tk.Label(self.topFrame, text="  Account Setting", bg='white', font='arial 21', fg='black')
        heading.place(x=290, y=30)

        #account infor display
        usernameLabel = tk.Label(self.bottomFrame, text="Username :  " + self.user.username, bg='#e0f0f0', font='arial 16')
        usernameLabel.place(x=10, y=10)


        passwordlable = tk.Label(self.bottomFrame, text="Password", bg='#e0f0f0', font='arial 16')
        passwordlable.place(x=10, y=80)

        self.passwordEntry = tk.Entry(self.bottomFrame, bg='white', font='arial 16', show='*')
        self.passwordEntry.insert(tk.END, self.user.password)
        self.passwordEntry.place(x=200, y=80)

        passwordChange = tk.Button(self.bottomFrame, text='Change', command=self.change_pwd)
        passwordChange.place(x=560, y=80)

        self.passwordShow = tk.Button(self.bottomFrame, text='Show', command=self.show_pwd)
        self.passwordShow.place(x=480, y=80)

        phoneLable = tk.Label(self.bottomFrame, text="Phone Number", bg='#e0f0f0', font='arial 16')
        phoneLable.place(x=10, y=150)

        self.phoneEntry = tk.Entry(self.bottomFrame, bg='white', font='16')
        self.phoneEntry.place(x=200, y=150)
        self.phoneEntry.insert(tk.END, self.user.phone)

        phoneChange = tk.Button(self.bottomFrame, text='Change', command=self.change_phone)
        phoneChange.place(x=560, y=150)

    def show_pwd(self):
        if self.passwordEntry['show'] == '*':
            self.passwordEntry['show'] = ''
            self.passwordShow['text'] = 'Hide'
        else:
            self.passwordEntry['show'] = '*'
            self.passwordShow['text'] = 'Show'

    def change_phone(self):
        res = mb.askquestion('Change number phone', 'Do you want to change your phone number?')
        if res == 'yes':
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Login).filter(Login.username == self.user.username).first()

            user.phone = self.phoneEntry.get()
            self.phoneEntry.delete(0, tk.END)
            self.phoneEntry.insert(0, user.phone)

            session.commit()
            # self.user = session.query(Login).filter(Login.username == user.username).first()


    def change_pwd(self):
        res = mb.askquestion('Change number password', 'Do you want to change your password?')
        if res == 'yes':
            Session = sessionmaker(bind=engine)
            session = Session()
            user = session.query(Login).filter(Login.username == self.user.username).first()

            user.password = self.passwordEntry.get()
            self.passwordEntry.delete(0, tk.END)
            self.passwordEntry.insert(0, user.password)
            self.user = user
            session.commit()

