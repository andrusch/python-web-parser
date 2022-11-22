from bs4 import BeautifulSoup
import re
from lib import *

load_envs()

def parse_jcrew_product_page(html: str):
    products =[]
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find_all(name="ul", attrs={"data-qaid": "arrProductListItem0ArrayWrapper"})
    for tag in section:
        for list_item in tag.findAll('li'): 
            product = list_item.find(name="h2")
            price = list_item.find(attrs={"data-qaid": re.compile('PriceWasFormattedPrice')})
            if product and price:
                print(product.text)
                print(price.text)
                products.append({"price": price.text, "product": product.text})
            else:
                print('-----------------------------------------')
                print(list_item)
                print('-----------------------------------------')
    return products

if __name__ == "__main__":
    url = "https://www.jcrew.com/all/womens?intcmp=newHP_oneup_1_null_allwomens&om_i=newHP_p1"
    html = get_website(url)
    for result in parse_jcrew_product_page(html):
        save_to_supabase(url, result["product"], result["price"])
    
