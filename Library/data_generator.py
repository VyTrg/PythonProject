

from Library.library_management import Login, Book, engine, Category, BookCategory, Author
from library_management import session
from faker import Faker
import csv
import requests

from bs4 import BeautifulSoup


from random import randint
import random

faker = Faker()



def book_author_data():
    for i in range(1, 41):
        book = session.query(Book).filter(Book.book_id == randint(1, session.query(Book).count() - 1)).first()
        entry = {
            'author_id': i,
            'name': faker.name(),
            'book_id': book.book_id
        }
        book_author = Author(book_id= entry['book_id'], author_id= entry['author_id'], name= entry['name'])
        session.add(book_author)
        session.commit()

def login_data():
    role = ["reader", "librarian"]
    for i in range(1, 41):
        entry = {
            'username': random.choice(role) + randint(),
            'password': faker.password(),
            'status': True,
            'phone': faker.phone_number(),
            'name': faker.name()
        }
        login = Login(username=entry['username'], password=entry['password'], status=entry['status'], phone=entry['phone'], name=entry['name'])
        session.add(login)
        session.commit()


def book_data():
    cnt = 1
    for i in range(1, 10):
        url = f"https://books.toscrape.com/catalogue/page-{i}.html"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')
        ol = soup.find('ol')
        articles = ol.find_all('article', class_='product_pod')
        for article in articles:
            image = article.find('img')
            title = image.attrs['alt']
            image_url = image.attrs['src']
            entry = {
                        'book_id': cnt,
                        'isbn': faker.isbn10(),
                        'title': title,
                        'year': faker.year(),
                        'quantity': randint(1, 40),
                        'image': f'{cnt}.jpg'
                    }
            r = requests.get("https://books.toscrape.com/" + image_url[2:]).content
            try:
                r = str(r, 'utf-8')
            except UnicodeDecodeError:
                with open(f"assets/book_image/{cnt}.jpg", "wb+") as f:
                    f.write(r)
            cnt = cnt + 1
            book = Book(book_id=entry['book_id'], title=entry['title'], year=entry['year'], isbn=entry['isbn'], image=entry['image'], quantity=entry['quantity'])
            session.add(book)
            session.commit()


def category_data():
    url = f"https://books.toscrape.com/catalogue/page-1.html"
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')
    a_tags = soup.find_all('a')
    categories = []
    for a_tag in a_tags:
        if "category" in a_tag.attrs['href']:
            link_text = a_tag.text.strip()
            categories.append(link_text)
    categories.pop(0)
    cnt = 1
    for i in categories:
        category = Category(category_id=cnt, category_name=i)
        session.add(category)
        session.commit()
        cnt = cnt + 1

def book_category_data():
    pass

def issue_return_detail_data():
    pass

if __name__ == "__main__":
    # book_data()
    # book_author_data()
    # login_data()
    # category_data()
    pass
