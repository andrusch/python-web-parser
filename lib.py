

import hashlib
import requests
from supabase import create_client, Client
import json
import os
import re

def load_envs():
    txt = read_from_file('local_settings.json')
    d = json.loads(txt)
    for key in d:
        print(key)
        os.environ[key] = d[key]

def get_website(url: str, addUserAgentString: bool=False):
    filename = f'cache/{calculate_filename(url)}.html'
    html = ''
    try:
        print(f'Retrieving from cache.')
        html = read_from_file(filename)
    except:
        print(f'Reading from: {url}')
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        html = response.text
        save_to_file(filename, html)
    return html

def save_to_file(filename: str, data: str):
    with open(filename, 'w') as my_data_file:
        my_data_file.write(data)

def read_from_file(filename: str):
    with open(filename, "r") as txt_file:
        return txt_file.read()

def calculate_filename(url: str):
    hash_object = hashlib.sha1(url.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def save_to_supabase(url: str, product: str, price: str):
    SUPABASE_URL = os.environ['SUPABASE_API']
    SUPABASE_KEY = os.environ['SUPABASE_API_KEY']
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    price = re.sub("[^0-9,\.]", "", price)
    print(url)
    print(product)
    print(price)
    data = supabase.table("product_prices").insert({"product":product, "site": url, "price": price}).execute()
    assert len(data.data) > 0

