import time
# this scrapes books.toscrape.com title, price, rating of all 1000 books
# and saves them to books.csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

titles = []
prices = []
ratings = []

for page in range(1, 51):
    if page == 1:
        url = 'https://books.toscrape.com/'
    else:
        url = 'https://books.toscrape.com/catalogue/page-' + str(page) + '.html'

    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating = book.find('p', class_='star-rating')['class'][1]

        titles.append(title)
        prices.append(price)
        ratings.append(rating)

    print("Page", page, "done -", len(books), "books")
    time.sleep(0.5)

df = pd.DataFrame({'Title': titles, 'Price': prices, 'Rating': ratings})
df.to_csv('books.csv', index=False, encoding='utf-8-sig')

print(len(df), "books saved")