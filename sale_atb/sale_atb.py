import requests
from bs4 import BeautifulSoup
import time
import json

page = requests.get('https://www.atbmarket.com/hot/akcii/economy')
soup = BeautifulSoup(page.content, features='html.parser')


def Products():
    allProducts_disc = soup.find_all('div', class_='promo_info')
    result = []
    result.append({
        'shopName': soup.find('div', class_='hot_line_block').text[39:-14].replace(" ", "")
        # search for the store name on the page                 #the replace method is used for good text design

    })
    for i in allProducts_disc:
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
        result.append({
            'promotions_information': [{
                'productName': nameProduct,
                'oldPrice': price,
                'newPrice': str(newPrice).replace(' ', '').replace('\n', '') + "." + i.find('div',
                                                                                            class_='promo_price').find(
                    'span').text,
                # the replace method is used for good text design
                # that the new price came out in a format for example 20.00 instead of 2000
                'discount': str(discount).replace(" ", ""),
            }]

        })

    return result


start = time.perf_counter()
process = Products()
print('Forecast gathering time: {}'.format(
    time.perf_counter() - start))  # additionally searching for time, it was interesting to learn

with open('Products-{}.json'.format(time.strftime('%Y-%m-%d')), 'w') as jsonFile:
    json.dump(process, jsonFile)
