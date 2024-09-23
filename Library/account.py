import tkinter as tk

class AccountSetting(tk.Toplevel):
    def __init__(self, user):
        tk.Toplevel.__init__(self)
        self.title("Account Setting")
        self.geometry("650x500")
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
        heading = tk.Label(self.topFrame, text="  Account Setting", bg='white', font='arial 21 bold', fg='black')
        heading.place(x=290, y=30)

        #account infor display
        usernameLabel = tk.Label(self.bottomFrame, text="Username :  " + self.user.username, bg='#e0f0f0', font='arial 16 bold')
        usernameLabel.place(x=10, y=10)


        passwordlable = tk.Label(self.bottomFrame, text="Password", bg='#e0f0f0', font='arial 16 bold')
        passwordlable.place(x=10, y=80)

        self.passwordEntry = tk.Entry(self.bottomFrame, bg='white', font='arial 16 bold', show='*')
        self.passwordEntry.insert(tk.END, self.user.password)
        self.passwordEntry.place(x=200, y=80)

        passwordChange = tk.Button(self.bottomFrame, text='Change')
        passwordChange.place(x=560, y=80)

        self.passwordShow = tk.Button(self.bottomFrame, text='Show', command=self.show_pwd)
        self.passwordShow.place(x=480, y=80)

        phoneLable = tk.Label(self.bottomFrame, text="Phone Number", bg='#e0f0f0', font='arial 16 bold')
        phoneLable.place(x=10, y=150)

        phoneEntry = tk.Entry(self.bottomFrame, bg='white', font='arial 16 bold')
        phoneEntry.place(x=200, y=150)
        phoneEntry.insert(tk.END, self.user.phone)

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
        pass
