import requests
import re
from bs4 import BeautifulSoup
from consts import AMAZON_URL, HEADERS, API_KEY, API_URL
from jobs.cron import cron_job

def scrape_product(href):
    categories = []
    features = []

    payload = {
        "api_key": API_KEY,
        "url": AMAZON_URL + href
    }  ## Creating payload for ScrapperAPI

    while True:

        response = requests.get(API_URL, params=payload)  ### Passing the API_KEY, Amazon Product URL to API

        if response.status_code >= 500: ### Checking if the API call has failed
            continue
        else:
            break

    soup = BeautifulSoup(response.content, features="lxml") ### Using beautiful soup to read reponse content in HTML

    title = soup.select("#productTitle")[0].get_text().strip() ## Getting the product title from the HTML content

    if len(soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")) > 0:
        for li in soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
            if li.get_text().strip() != '›' and li.get_text().strip() != '‹':
                categories.append(li.get_text().strip())   ### Making a list of the product categories
    else:
        categories.append('None')

    if len(soup.select("#feature-bullets ul.a-unordered-list")) > 0:
        for li in soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
            features.append(li.get_text().strip())  ### Making a list of the product features
    else:
        features.append('None')

    if len(soup.select("#priceblock_ourprice")) > 0:
        price = soup.select("#priceblock_ourprice")[0].get_text() ### Getting the price of product
    else:
        price = 'None'  ### Setting price as None if it is not mentioned

    if len(soup.select("#sellerProfileTriggerId")) > 0:
        seller = AMAZON_URL + soup.select("#sellerProfileTriggerId")[0].get('href') ###Getting the seller info of the product
    else:
        seller = 'None' ### Setting seller info as None if it is not avaliable

    if len(soup.select("#availability")[0].get_text()) > 0:
        availability = soup.select("#availability")[0].get_text().replace('\n','') ###Getting the availability of the product
    else:
        availability = 'None' ### Setting availability as None if it is not mentioned

    if len(soup.select("#acrCustomerReviewText")[0].get_text().split()[0].replace(',','')) > 0:
        review_count = int(soup.select("#acrCustomerReviewText")[0].get_text().split()[0].replace(',','')) ###Getting the customer reviews count of the product
    else:
        review_count = 0

    product_id = re.findall('(/dp/)([A-Za-z0-9]*)(?=&)?',href)  ## Getting ASIN of the prduct from the URL

    if len(product_id) > 0:
        product_id = product_id[0][1]
    else:
        product_id = title ## Setting the ASIN as product name if it is not there in the URL

    productjson = {
        'id': product_id,
        'title': title, 
        'categories': categories, 
        'features': features, 
        'price': price, 
        'review_count': review_count,
        'seller': seller,
        'availability': availability
        }  ### Creating a JSON object of the product details

    cron_job(productjson) #### Inserting the data into the tables
    print(productjson)