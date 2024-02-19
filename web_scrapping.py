import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

res = requests.get('https://thundergroup.com/all-products/melamine-western/victoria.html')
soup= BeautifulSoup(res.text,'html')


def get_names_and_img_urls(soupss):
    product_names=[]
    product_images=[]
    for i in soup.findAll("strong", class_="product name product-item-name"):
        product_names.append(i.text.strip())
    for i in soup.findAll("img", class_="product-image-photo"):
        product_images.append(i['src'])

        df1 = pd.DataFrame(
                                    {'name': product_names
                                    })
        df2 = pd.DataFrame(
                                    {
                                    'image': product_images
                                    })
        
    return pd.concat([df1, df2], axis=1)


df1 = get_names_and_img_urls(soup)

links = soup.findAll("a", class_="product-item-link", href=True)
link_urls=[]
for i in links:
    link_urls.append(i['href'])



soupss=[]
def make_soups(urlss):
    for url in urlss: 
        res=requests.get(url)
        soup= BeautifulSoup(res.text,'html')
        soupss.append(soup)
    return soupss

soups=make_soups(link_urls)

#skus and details
def get_skus_and_details(soupss):
    skus_list = []
    details_list = []
    for soup in soupss:
        for i in soup.findAll("div", itemprop="sku"):
            skus_list.append(i.text)
        for i in soup.findAll("div", class_="product attribute description"):
            details_list.append(i.text.strip)
        df = pd.DataFrame(
                                    {'sku': skus_list,
                                    'details': details_list
                                    })
    return df

df2 = get_skus_and_details(soupss)

df3 = pd.concat([df1, df2], axis=1)

def get_more_info(soupss):
    more_info_list = []
    more_info_2 = []
    for soup in soupss:
        for i in soup.findAll("th", class_="col label"):
            more_info_list.append(i.text)
        
        for i in soup.findAll("td", class_="col data"):
            more_info_2.append(i.text)
        df = pd.DataFrame(
                                    {'title': more_info_list,
                                     'value': more_info_2
                                    })
    return df


df4 = get_more_info(soupss)

print(df4)

print(df3)
