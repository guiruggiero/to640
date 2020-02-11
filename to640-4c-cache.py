# TO 640, worksheet 4C (with cache)
# Developed by Gui Ruggiero

import requests
import json
from bs4 import BeautifulSoup
from time import sleep

# Trying to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# If no file, create a dictionary
except:
    CACHE_DICTION = {}

# Main cache function
def make_request_using_cache(url):
    unique_ident = url

    # Data already in cache
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    # Fetch data and add it to cache
    else:
        # print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        sleep(5)
        return CACHE_DICTION[unique_ident]

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
    page_text = make_request_using_cache(url)
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

# Checking if all 1000 books were scraped
print("names list = " + str(len(names)))
print("prices list = " + str(len(prices)))

# Exporting CSV
j = 0
with open("products-cache.csv", "w") as f:
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