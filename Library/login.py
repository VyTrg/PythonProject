import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from library_management import Login

import reader

import librarian

class LoginWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Login")
        self.window.geometry("250x180")


        # widget
        self.username_label = tk.Label(self.window, text="Username:")
        self.password_label = tk.Label(self.window, text="Password:")
        self.username_entry = tk.Entry(self.window)
        self.password_entry = tk.Entry(self.window, show="*")

        self.login_button = tk.Button(self.window, text="Login", command=self.login)


        self.login_status = tk.Label(self.window, text="", fg="black")


        self.username_label.grid(row=0, column=2, padx=5, pady=5, sticky="E")
        self.username_entry.grid(row=0, column=3, padx=5, pady=5)
        self.password_label.grid(row=1, column=2, padx=5, pady=5, sticky="E")
        self.password_entry.grid(row=1, column=3, padx=5, pady=5)
        self.login_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        self.login_status.grid(row=3, column=2, columnspan=2, padx=10, pady=5)

    def login(self):
        engine = create_engine('sqlite:///library_management.db')

        Session = sessionmaker(bind=engine)
        session = Session()

        username = session.query(Login).filter(Login.username == self.username_entry.get()).first() #first record
        password = session.query(Login).filter(Login.password == self.password_entry.get()).first()
        if  username is not None and  password is not None:
            if "reader" in username.username: # reader role
                messagebox.showinfo("Login Successful", "You have successfully logged in, Reader!")
                self.window.destroy()
                reader.page()
            elif "librarian" in username.username: #librarian role
                messagebox.showinfo("Login Successful", "You have successfully logged in, Librarian!")
                self.window.destroy()
                librarian.page()
        else:
            messagebox.showinfo("Login Failed", "Please try again!")


def page():
     window = tk.Tk()
     LoginWindow(window)
     window.mainloop()


if __name__ == '__main__':
    page()