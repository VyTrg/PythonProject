
import tkinter as tk
import account
from library_management import session, IssueReturnDetail, Book


import login


class ReaderWindow:
    def __init__(self, window, user):
        self.window = window
        self.window.title("Reader")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        self.user = user

        book_lists = session.query(IssueReturnDetail).filter(IssueReturnDetail.username == self.user.username).all()
        for book in book_lists:
            print(book.book_id)
        mainFrame = tk.Frame(self.window)
        mainFrame.pack()

        topFrame = tk.Frame(mainFrame, width=1000, height=70, bg="#f8f8f8", padx=20, relief=tk.SUNKEN, borderwidth=2)
        topFrame.pack(side=tk.TOP, fill=tk.X)

        centerFrame = tk.Frame(mainFrame, width=1000, relief=tk.RIDGE, bg="#e0f0f0", height=530)
        centerFrame.pack(side=tk.TOP)
        leftFrame = tk.Frame()


        # self.iconlogout = tk.PhotoImage(file="assets/icons/logout.png")
        self.buttonlogout = tk.Button(topFrame, text="Logout", compound=tk.RIGHT, font='arial 12 bold',
                                      command=self.logout)
        self.buttonlogout.pack(side=tk.RIGHT, padx=10)

        # account button
        self.iconaccount = tk.PhotoImage(file="assets/icons/user.png", height=50, width=50)
        self.buttonaccount = tk.Button(topFrame, text="Account", image=self.iconaccount, compound=tk.LEFT,
                                       font="arial 12", command=self.account)
        self.buttonaccount.pack(side=tk.LEFT, padx=10)

        # welcome user
        welcome_label = tk.Label(centerFrame, text="Welcome, " + str(self.user.username), font="arial 12", bg="#e0f0f0")
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


def run(user):
    window = tk.Tk()
    ReaderWindow(window, user)
    window.mainloop()
