from flask import Flask, jsonify, request
from data_atb import ProductsInfo
import time

app = Flask(__name__)

cache = None
lastTime = None


def getCache():
    global cache, lastTime

    realTime = time.perf_counter()
    if cache == None or realTime - lastTime > 12 * 60 * 60:
        print("data from the website")

        lastTime = realTime
        cache = ProductsInfo.Products()
    else:
        print("data from the cache")
    return cache


@app.route('/promotions/<nameShop>/', methods=['GET'])
def promotions(nameShop):
    product = getCache()
    nameShop = product['shopName']  # I add the name of the store to the url.
    print('withdrawal of all products at a discount')
    return jsonify(product)


@app.route('/promotions/<nameShop>/withDiscount/', methods=['POST'])
def withDisc(nameShop):
    product = getCache()
    nameShop = product['shopName']
    try:
        dataPOST = request.get_json()
    except TypeError:
        print("body is empty.  Enter data!")
    discountMoreThan = int(dataPOST['discountMoreThan'])
    withDiscount = {}  # I create a dictionary with a list and add data for better design with the POST method.
    products = []
    for i in product['promotions']:
        if i['discount'] > discountMoreThan:
            products.append(i)
    withDiscount['promotions'] = products
    print('found discounts with a percentage greater than ' + str(discountMoreThan))
    return jsonify(withDiscount)


def main():
    app.run()


if __name__ == '__main__':
    main()
