import requests
from bs4 import BeautifulSoup


page = requests.get('https://www.atbmarket.com/hot/akcii/economy')
soup = BeautifulSoup(page.content, features='html.parser')

class ProductsInfo():
    @staticmethod
    def Products():
        allProducts_disc = soup.find_all('div', class_='promo_info')
        result = {}
        result['shopName'] = soup.find('div', class_='hot_line_block').text[39:-14].strip()

        # slice [39:-14] I used to get the name of the store from the variable
        # soup (from the front I cut the text before the name and behind the same)
        results = []
        for i in allProducts_disc:
            price = i.find('span', class_='promo_old_price')
            if price:
                price = price.get_text(strip=True)
            else:
                price = "empty"

            discount = i.find('div', class_='economy_price')
            if discount:
                discount = discount.text[11:-2]
            else:
                discount = 0

            nameProduct = i.find('span', class_='promo_info_text').get_text(strip=True)
            newPrice = i.find('div', class_='promo_price').text[:-7]
            results.append({

                'productName': nameProduct,
                'oldPrice': price,
                'newPrice': str(newPrice).strip() + "." + i.find('div',
                                                                 class_='promo_price').find(
                    'span').text,

                'discount': int(discount),

            })
        result['promotions'] = results

        return result
