import requests
import json
from bs4 import BeautifulSoup
import time

URL = 'https://evrika.com/catalog'

def get_categories(URL):
    r = requests.get(URL, verify=False)
    soup = BeautifulSoup(r.text)
    parent_categories = [(i['href'], i.text) for i in soup.find_all('a', class_='category-name')]
    return parent_categories

res_list = []

for parent_cat_link, cat_name in get_categories(URL):
    for sub_cat_link, subcat_name in get_categories(parent_cat_link):
        for sub_sub_cat_link, sub_sub_cat_name in get_categories(sub_cat_link):
            i = 1
            while True:
                try:
                    r = requests.get(sub_sub_cat_link + f'?page={i}', verify=False)
                    print(sub_sub_cat_link + f'?page={i}')
                    soup = BeautifulSoup(r.text)
                    # last card is bullshit
                    prod_details = [i for i in soup.find_all('div', class_='goods-tile')][:-1]
                    for prod_detail in prod_details:

                        # product details
                        name_tab = prod_detail.find('div', class_='goods-tile__name')
                        price = prod_detail.find('div', class_='cost__value').text

                        name = name_tab.text
                        link = name_tab.find('a')['href']
                        
                        res = {
                            'name': name, 
                            'price': price, 
                            'link': link,
                            'category': sub_sub_cat_name,
                            'sub_category': subcat_name,
                            'parent_category': cat_name
                            }

                        print(res)
                            
                        res_list.append(res)
                    # go to next page
                    i += 1
                    print(i)
                except Exception as e:
                    print(e)
                    break

print(len(res_list))
            
    