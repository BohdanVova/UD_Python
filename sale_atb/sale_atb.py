import requests
from bs4 import BeautifulSoup
import time
import json

page = requests.get('https://www.atbmarket.com/hot/akcii/economy')
soup = BeautifulSoup(page.content, features='html.parser')


def Products():
    allProducts = soup.find_all('div', class_='promo_info')
    resultJson = []
    resultJson.append({
        'shopName': soup.find('div', class_='hot_line_block').text[39:-14]  # search for the store name on the page

    })
    for i in allProducts:
        price = i.find('span', class_='promo_old_price')
        if price:
            price = price.get_text(strip=True)
        else:
            price = "empty"

        discount = i.find('div', class_='economy_price')
        if discount:
            discount = discount.text[11:]
        else:
            discount = "empty"

        nameProduct = i.find('span', class_='promo_info_text').get_text(strip=True)
        newPrice = i.find('div', class_='promo_price').text[:-7]
        resultJson.append({
            'promotions_information': [{
                'productName': nameProduct,
                'oldPrice': price,
                'newPrice': str(newPrice) + "." + i.find('div', class_='promo_price').find('span').text,
                # that the new price came out in a format for example 20.00 instead of 2000
                'discount': str(discount),
            }]

        })
        
    return resultJson


start = time.perf_counter()
forecast = Products()
print('Forecast gathering time: {}'.format(
    time.perf_counter() - start))  # additionally searching for time, it was interesting to learn

with open('Products-{}.json'.format(time.strftime('%Y-%m-%d')), 'w') as jsonFile:
    json.dump(forecast, jsonFile)
