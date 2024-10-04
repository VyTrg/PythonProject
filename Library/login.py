import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

from library_management import session

from library_management import Login

import reader


class WelcomeWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("QUẢN LÍ THƯ VIỆN")
        self.window.geometry("1000x600")


        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True)


        left_frame = tk.Frame(main_frame, bg="#00FFFF")
        left_frame.grid(row=0, column=0, sticky="nsew")


        right_frame = tk.Frame(main_frame, bg="#36454F")
        right_frame.grid(row=0, column=1, sticky="nsew")


        try:
            self.dog_image = PhotoImage(file='assets/image/thuvienimage.png')
            self.dog_image_label = tk.Label(left_frame, image=self.dog_image, bg="#00FFFF")
            self.dog_image_label.pack(expand=True, fill=tk.BOTH)
        except tk.TclError as e:
            print(f"Error: {e}")


        title_label = tk.Label(right_frame, text="QUẢN LÍ THƯ VIỆN ", font=('Comic Sans MS', 25, 'bold'),
                               bg="#36454F", fg="#FFFFFF")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=30, sticky='ne')

        user_label = tk.Label(right_frame, text="Username  :", padx=10, font=('Comic Sans MS', 15, 'bold'),
                              bg="#36454F", fg="#FFFFFF")
        user_label.grid(row=0, column=0, columnspan=2, pady=(100, 10), padx=20, sticky='w')

        self.user_entry = tk.Entry(right_frame)
        self.user_entry.grid(row=0, column=1,columnspan=2, pady=(160, 10), padx=90, sticky='ne')

        password_label = tk.Label(right_frame, text="Password  :", padx=50, font=('Comic Sans MS', 15, 'bold'),
                              bg="#36454F", fg="#FFFFFF")
        password_label.grid(row=0, column=0, columnspan=2, pady=(200, 10), padx=0, sticky='w')

        self.password_entry = tk.Entry(right_frame, show="*")
        self.password_entry.grid(row=0, column=1, columnspan=2, pady=(210, 10), padx=90, sticky='ne')

        login_button = tk.Button(right_frame, text="👉 Log In", font=('Arial', 20, 'bold'), command=self.login,
                                 bg="#40E0D0", fg="white", padx=20, pady=5)
        login_button.grid(row=1, column=1, pady=10, padx=130, sticky='e')


        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        right_frame.grid_columnconfigure(1, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)

        self.dog_image_label.config(width=550, height=600)


    def login(self):

        # Session = sessionmaker(bind=engine)
        # session = Session()
        username = session.query(Login).filter(self.user_entry.get() == Login.username).first()

        try:

            if username is not None and username.password == self.password_entry.get():
                if "reader" in username.username:  # reader role
                    messagebox.showinfo("Login Successful", "You have successfully logged in, Reader!")
                    self.window.destroy()
                    reader.run(username)
                if "librarian" in username.username:  # librarian role
                    messagebox.showinfo("Login Successful", "You have successfully logged in, Librarian!")
            else:
                messagebox.showinfo("Login Failed", "Username or Password is incorrect!")
        except ValueError as ve:
            messagebox.showinfo("Login Failed", str(ve))



def run():
    window = tk.Tk()
    WelcomeWindow(window)
    window.mainloop()


if __name__ == '__main__':
    window = tk.Tk()
    WelcomeWindow(window)
    window.mainloop()