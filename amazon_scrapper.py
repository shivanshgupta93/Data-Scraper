import requests
from bs4 import BeautifulSoup
from consts import AMAZON_URL, HEADERS, API_KEY, API_URL
from product_scrapper import scrape_product
import time

def scrape_amazon(keywords):

    count = 0  #### Setting count to take only valid 6 product results

    url = AMAZON_URL + "/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + keywords.replace('_','+')  ## Searching for the product in amazon

    payload = {
        "api_key": API_KEY,
        "url": url
    } ## Creating payload for ScrapperAPI

    while True:

        response = requests.get(API_URL, params=payload)  ### Passing the API_KEY, Amazon Search URL to API

        if response.status_code >= 500: ### Checking if the API call has failed
            continue
        else:
            break

    soup = BeautifulSoup(response.content, "lxml") ### Using beautiful soup to read reponse content in HTML
    links = soup.find_all('a', {'class': 'a-link-normal a-text-normal'}) ### Getting all the links in the search results
    for l in links:
        href = l.get('href')
        if keywords.replace('_','+') in href and count < 6:   ### Checking if the product name exists in the product url
            print(href)
            scrape_product(href)  ### Calling script to scrape the data of a product
            count += 1