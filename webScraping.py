from numpy import imag
import requests
from bs4 import BeautifulSoup
file = open("x.html", mode="r", encoding='utf-8')
htmlContent = file.read()
soup = BeautifulSoup(htmlContent, 'html.parser')

"""
# Commonly used types of objects: Tag, NavigableString, BeautifulSoup, Comment
print(soup.title) # Get the title of the webpage
anchors = soup.find_all('a') #Get all the anchor tags on the page, use find function to get the first one only
print(anchors[0]['class']) #This is how you get the class of any element
print(soup.find_all("a", class_='product__wrapper')) #Find all the anchor tags with the specified class
print(soup.find('p').get_text()) #Get the text from all of the p tags of the page
"""

img = soup.select('a.product__wrapper > div.plp-product > div.sc-hKMtZM.elMeKu.Product__ProductImage-sc-11dk8zk-2.jPRoxC > img.sc-iBkjds')
images = list(map(lambda d: d.get('src'), img))

nameDivs = soup.select('a.product__wrapper > div.plp-product > div.Product__DetailContainer-sc-11dk8zk-3.ksQHQi >div.Product__ProductName-sc-11dk8zk-4.dNDTui')
names = list(map(lambda d: d.get_text(), nameDivs))

qtySpans = soup.select('a.product__wrapper > div.plp-product > div.Product__DetailContainer-sc-11dk8zk-3.ksQHQi > span.variant_text_only.plp-product__quantity--box')
qty = list(map(lambda d: d.get_text(), qtySpans))

priceDivs = soup.select('a.product__wrapper > div.plp-product > div.Product__DetailContainer-sc-11dk8zk-3.ksQHQi > div.Product__PriceAtcContainer-sc-11dk8zk-1.klnIGW > div.ProductPrice__PriceContainer-sc-14194u2-0.iKlIZr > div.ProductPrice__Price-sc-14194u2-1.eJcLXJ')
price = list(map(lambda d: d.get_text()[1:], priceDivs))

products = list(zip(images, names, qty, price))

markup = """
<div class="card">
    <img src="{}" alt="" class="image">
    <h3 class="title">{}</h3>
    <div class="info">
        <span class="info">{}</span>
        <span class="price">{}</span>
    </div>
    <div class="form">
        <input type="number" name="1" id="1" maxlength="2">
        <i class="icon icon-logo"></i>
        <i class="icon icon-logo"></i>
        <i class="icon icon-logo"></i>
    </div>
</div>
"""

copy = ''

for product in products:
    copy = copy + "\n" + markup.format(product[0], product[1], product[2], product[3])

print(copy)
