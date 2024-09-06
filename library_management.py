from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Login(Base): 
    __tablename__ = 'login'
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    phone = Column(String)
    
class Category(Base): 
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False)

class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer)
    quantity = Column(Integer, default=0)
    image = Column(String) # Image or String 

class Author(Base):
    __tablename__ = 'book_author'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id')) # foreignkey with book
    
    book = relationship("Book", back_populates="authors")
    
Book.authors = relationship("Author", order_by=Author.author_id, back_populates="book")

class BookCategory(Base):
    __tablename__ = 'book_category'
    book_category_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.book_id'))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    
    book = relationship("Book", back_populates="categories")
    category = relationship("Category", back_populates="books")
    
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
    
Book.requests = relationship("BookRequest", back_populates="book")
Login.requests = relationship("BookRequest", back_populates="user")

class IssueReturn(Base):
    __tablename__ = 'issue_return'
    issue_return_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)


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

IssueReturn.details = relationship("IssueReturnDetail", back_populates="issue_return")
Book.issue_details = relationship("IssueReturnDetail", back_populates="book")


if __name__ == '__main__' :
    engine = create_engine('sqlite:///library_management.db')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()