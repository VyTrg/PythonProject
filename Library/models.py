

# from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_imageattach.entity import Image, image_attachment
#
# Base = declarative_base()
#
# class book(Base):
#     __tablename__ = 'book'
#     book_id = Column(Integer, primary_key=True)
#     isbn = Column(String)
#     title = Column(String)
#     year = Column(Integer)
#     quantity = Column(Integer)
#     image = image_attachment('book_image')
#
#     def __init__(self, book_id, isbn, title, year, quantity, image):
#         self.book_id = book_id
#         self.isbn = isbn
#         self.title = title
#         self.year = year
#         self.quantity = quantity
#         self.image = image
#
# class book_author(Base):
#     __tablename__ = 'book_author'
#     author_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     book_id = Column(Integer, ForeignKey('book.book_id'))
#
#     def __init__(self, name, book_id, author_id):
#         self.name = name
#         self.book_id = book_id
#         self.author_id = author_id
#
# class book_image(Base, Image):
#     __tablename__ = 'book_image'
#     book_id = Column(Integer, ForeignKey('book.book_id'))
#
#
#     def __init__(self, book_id, image):
#         self.book_id = book_id
#         self.image = image