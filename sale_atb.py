import requests
from bs4 import BeautifulSoup
import time
import json

page = requests.get('https://www.atbmarket.com/hot/akcii/economy')
soup = BeautifulSoup(page.content, features='html.parser')
resultJson = []
resultJson.append({
    'shopName' : 'ATБ',
})

def Products():
    allProducts = soup.find_all('div', class_='promo_info')
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
        newPrice = i.find('div', class_='promo_price').text[:-4]
        resultJson.append({
            'promotion_information' : [{
            
            'name': nameProduct,
            'oldPrice': price,
            'newPrice': int(newPrice),
            'discount': str(discount),
            }]
        })



    return resultJson

start = time.perf_counter()
forecast = Products()
print('Forecast gathering time: {}'.format(time.perf_counter() - start))

with open('Products-{}.json'.format(time.strftime('%Y-%m-%d')), 'w') as jsonFile:
    json.dump(forecast, jsonFile)