


from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Login(Base): 
    __tablename__ = 'login'
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    status = Column(Boolean, default=True) # operating:True or closed:False
    phone = Column(String)

    def __init__(self, username, password, status, phone):
        self.username = username
        self.password = password
        self.status = status
        self.phone = phone


    
class Category(Base): 
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False)

    def __init__(self, category_id, category_name):
        self.category_name = category_name
        self.category_id = category_id


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer)
    quantity = Column(Integer, default=0)
    image = Column(String) # Image or String

    def __init__(self, book_id, isbn, title, year, quantity, image):
        self.book_id = book_id
        self.title = title
        self.year = year
        self.quantity = quantity
        self.image = image
        self.isbn = isbn

class Author(Base):
    __tablename__ = 'book_author'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id')) # foreignkey with book
    
    book = relationship("Book", back_populates="authors")

    def __init__(self, author_id, name, book_id):
        self.author_id = author_id
        self.name = name
        self.book_id = book_id
    
Book.authors = relationship("Author", order_by=Author.author_id, back_populates="book")

class BookCategory(Base):
    __tablename__ = 'book_category'
    book_category_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    
    book = relationship("Book", back_populates="categories")
    category = relationship("Category", back_populates="books")

    def __init__(self, book_id, category_id, book_category_id, category, book):
        self.book_id = book_id
        self.category_id = category_id
        self.book_id = book_id
        self.category = category
        self.book = book
        self.book_category_id = book_category_id

    
Book.categories = relationship("BookCategory", back_populates="book")
Category.books = relationship("BookCategory", back_populates="category")

class BookRequest(Base):
    __tablename__ = 'book_request'
    book_request_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    username = Column(String, ForeignKey('login.username'))
    issue_return = Column(Boolean, default=False)
    
    book = relationship("Book", back_populates="requests")
    user = relationship("Login", back_populates="requests")

    def __init__(self, book_id, username, issue_return):
        self.book_id = book_id
        self.username = username
        self.issue_return = issue_return
    
Book.requests = relationship("BookRequest", back_populates="book")
Login.requests = relationship("BookRequest", back_populates="user")

class IssueReturn(Base):
    __tablename__ = 'issue_return'
    issue_return_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)

    def __init__(self, username, issue_return_id):
        self.username = username
        self.issue_return_id = issue_return_id



class IssueReturnDetail(Base):
    __tablename__ = 'issue_return_detail'
    issue_return_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    issue_return_id = Column(Integer, ForeignKey('issue_return.issue_return_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    date_issue = Column(Date)
    date_return = Column(Date, nullable=True)
    status = Column(String, default='Issued')

    issue_return = relationship("IssueReturn", back_populates="details")
    book = relationship("Book", back_populates="issue_details")

    def __init__(self, book_id, date_issue, date_return, status, issue_return, book):
        self.book_id = book_id
        self.date_issue = date_issue
        self.date_return = date_return
        self.status = status
        self.issue_return = issue_return
        self.book = book


IssueReturn.details = relationship("IssueReturnDetail", back_populates="issue_return")
Book.issue_details = relationship("IssueReturnDetail", back_populates="book")


# if __name__ == '__main__' :
engine = create_engine('sqlite:///library_management.db')
Base.metadata.create_all(engine)

    
Session = sessionmaker(bind=engine)
session = Session()

    # login1 = Login('librarian1','1',True,'0900000')
    # login2 = Login('reader1','1',True,'0900001')
    # session.add(login1)
    # session.add(login2)
    #
    # session.commit()