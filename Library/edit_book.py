from tkinter import *
from tkinter import messagebox, Label, ttk, Button, Entry
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library_management.db')
cur = conn.cursor()

class EditBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Edit Book")
        self.resizable(False, False)

        # Fetching the list of books
        query = "SELECT * FROM book"
        books = cur.execute(query).fetchall()
        self.book_list = []
        for book in books:
            self.book_list.append(str(book[0]) + ' - ' + book[2])  # book_id - title

        # Frame
        self.topFrame = Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg="#fcc324")
        self.bottomFrame.pack(fill=X)

        try:
            self.edit_image = PhotoImage(file='../icons/edit2_book.png')
            self.edit_image_label = Label(self.topFrame, image=self.edit_image, bg="white")
            self.edit_image_label.pack(expand=True, fill=BOTH, padx =30, pady=30)

            # Add padding to the top
        except TclError as e:
            print(f"Error: {e}")

        # Labels and Combobox for selecting book
        self.label_select = Label(self.bottomFrame, text='Select Book:', font='verdana 14 bold', bg='#fcc324')
        self.label_select.place(x=60, y=15)
        self.combobox_books = ttk.Combobox(self.bottomFrame, width=60)
        self.combobox_books['values'] = self.book_list
        self.combobox_books.place(x=150, y=50)
        self.combobox_books.bind("<<ComboboxSelected>>", self.load_book_details)

        # Entry fields for book details
        self.label_isbn = Label(self.bottomFrame, text='ISBN:', font='verdana 12 bold', bg='#fcc324')
        self.label_isbn.place(x=230, y=100)
        self.entry_isbn = Entry(self.bottomFrame)
        self.entry_isbn.place(x=320, y=100)

        self.label_title = Label(self.bottomFrame, text='Title:', font='verdana 12 bold', bg='#fcc324')
        self.label_title.place(x=230, y=140)
        self.entry_title = Entry(self.bottomFrame)
        self.entry_title.place(x=320, y=140)

        self.label_year = Label(self.bottomFrame, text='Year:', font='verdana 12 bold', bg='#fcc324')
        self.label_year.place(x=230, y=180)
        self.entry_year = Entry(self.bottomFrame)
        self.entry_year.place(x=320, y=180)

        self.label_quantity = Label(self.bottomFrame, text='Quantity:', font='verdana 12 bold', bg='#fcc324')
        self.label_quantity.place(x=230, y=220)
        self.entry_quantity = Entry(self.bottomFrame)
        self.entry_quantity.place(x=320, y=220)

        # Button to save changes
        self.btn_save = Button(self.bottomFrame, text='SAVE CHANGE',font='verdana 14 bold', command=self.save_changes)
        self.btn_save.place(x=260, y=290)

    def load_book_details(self, event):
        """Load selected book details into entry fields."""
        selected_book = self.combobox_books.get()
        book_id = int(selected_book.split('-')[0])

        query = "SELECT * FROM book WHERE book_id = ?"
        book_details = cur.execute(query, (book_id,)).fetchone()

        if book_details:
            self.entry_isbn.delete(0, END)
            self.entry_isbn.insert(0, book_details[1])  # ISBN
            self.entry_title.delete(0, END)
            self.entry_title.insert(0, book_details[2])  # Title
            self.entry_year.delete(0, END)
            self.entry_year.insert(0, book_details[3])  # Year
            self.entry_quantity.delete(0, END)
            self.entry_quantity.insert(0, book_details[4])  # Quantity

    def save_changes(self):
        """Save changes made to the book details."""
        selected_book = self.combobox_books.get()
        if selected_book:
            book_id = int(selected_book.split('-')[0])
            isbn = self.entry_isbn.get()
            title = self.entry_title.get()
            year = self.entry_year.get()
            quantity = self.entry_quantity.get()

            if isbn and title and year and quantity.isdigit():
                try:
                    query = """UPDATE book SET isbn = ?, title = ?, year = ?, quantity = ?
                               WHERE book_id = ?"""
                    cur.execute(query, (isbn, title, int(year), int(quantity), book_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Book details updated successfully.")
                    self.destroy()  # Close the window after saving
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update book: {e}")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields correctly.")

if __name__ == '__main__':
    window = Tk()
    EditBook()  # You can open it directly for testing
    window.mainloop()
