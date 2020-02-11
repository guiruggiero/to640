# TO 640, worksheet 4C
# Developed by Gui Ruggiero

import requests
from bs4 import BeautifulSoup
from time import sleep

# Initializing lists
names = []
prices = []

# Scraping
for i in range(1, 51):
    # print(i)

    # Building link that will be scraped
    url = "http://books.toscrape.com/catalogue/page-" + str(i) + ".html"
    # print(url)

    # Getting HTML code
    page_text = requests.get(url).text
    # print(page_text)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    # print(page_soup)
    
    # Finding where book names are
    h3_names = page_soup.find_all("h3")
    # print(h3_names)

    # Extracting names
    for h3 in h3_names:
        name = h3.find("a")["title"]
        # print(name)
        names.append(name)
        # print(names)
    # print(len(names))

    # Finding where prices are
    p_prices = page_soup.find_all(class_ = "price_color")
    # print(p_prices)

    # Extracting prices
    for p in p_prices:
        price = p.text[2:]
        # print(price)
        prices.append(price)
        # print(prices)
    # print(len(prices))

    sleep(5)

# Checking if all 1000 books were scraped
print("names list = " + str(len(names)))
print("prices list = " + str(len(prices)))

# Exporting CSV
j = 0
with open("products.csv", "w") as f:
    # Creating header
    f.write("name,price")
    f.write("\n")

    # Exporting books
    for line in names:
        # print(line)
        # print(prices[j])
        f.write(line)
        f.write(",")
        f.write(prices[j])
        
        # Avoids blank last line
        j += 1
        if j != 1000:
            f.write("\n")
f.close()

# Checking if all 1000 books were exported
print("book count =", str(j))