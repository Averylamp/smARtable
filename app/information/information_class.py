API_KEY = "SEM3E447346A0C91AC10BE8A3CD493AD0C09"
API_SECRET = "N2QxYjM3MjEzZDI4MzgwOTI3YWQ5MmMzZDY4OGMxNWY"

from semantics3 import Products
from pprint import pprint

import json

def get_product_info(name):
    sem3 = Products(api_key=API_KEY, api_secret=API_SECRET)
    sem3.products_field("search", name)
    sem3.products_field("site", ["target.com", "samsclub.com", "walmart.com"])
    results = sem3.get()
    res = results['results']
    r = sorted(res, key=lambda s: -s['updated_at'])[0]
    pprint(r)
    j = {}
    j['name'] = r['name']
    j['price'] = r['price']
    j['image'] = r['images'][0]
    j['link'] = r['sitedetails'][0]['url']
    return j
