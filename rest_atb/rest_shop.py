from flask import Flask, jsonify, request
from data_atb import ProductsInfo

app = Flask(__name__)
product = ProductsInfo.Products()


@app.route('/promotions/<nameShop>/', methods=['GET'])
def promotions(nameShop):
    global product
    nameShop = product['shopName']
    print('withdrawal of all products at a discount')
    return jsonify(product)


@app.route('/promotions/<nameShop>/withDiscount/', methods=['POST'])
def withDisc(nameShop):
    global product
    nameShop = product['shopName']
    dataPOST = request.get_json()
    discountMoreThan = int(dataPOST['discountMoreThan'])
    withDiscount = {}  # I create a dictionary with a list and add data for better design with the POST method.
    products = []
    for i in product['promotions']:
        if i['discount'] > discountMoreThan:
            products.append(i)
    withDiscount['promotions'] = products
    print('derivation of specific products')
    return jsonify(withDiscount)


def main():
    app.run()


if __name__ == '__main__':
    main()
