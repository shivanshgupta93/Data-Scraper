import sys
from amazon_scrapper import scrape_amazon
from extract import extract_excel

def main(products):

    for product in products.split(','):   #### Spliting user input into a list of products
        print(product.strip())
        scrape_amazon(product)  ### Searching the product on the amazon
    
    extract_excel() ### Extracting all the tables data into a excel file

if __name__ == '__main__':
    products = sys.argv[1] ### Getting the user input which can be passed as follows:  
                                                            ##1. mobile_phones 
                                                            ##2. mobile_phones,digital_cameras
                                                            ##3. mobile_phones,digital_cameras,computer_accessories,printer,headsets
    main(products)