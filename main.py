from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from configs.config import Development, Production

app = Flask(__name__)

# configs

app.config.from_object(Development)

# sqlAlchemy instance

db = SQLAlchemy(app)

from models import *


# create table before any request is done

@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/inventory')
def inventory():
    inventories = InventoryModel.query.all()
    return render_template('inventory.html', inventories=inventories)


@app.route('/add', methods=['POST', 'GET'])
def insert_inventory():
    if request.method == 'POST':
        pn = request.form['product_name']
        pt = request.form['product_type']
        sn = request.form['serial_no']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        s = request.form['stock']
        rp = request.form['reorder_point']
        print(pn)
        print(pt)
        print(sn)
        print(sp)
        print(s)
        print(rp)
        product_one = InventoryModel(ProductName=pn, ProductType=pt, SerialNumber=sn, BuyingPrice=bp, SellingPrice=sp,
                                     Stock=s, ReorderPoint=rp)
        product_one.create_record()

        return redirect(url_for('inventory'))

        return render_template('inventory.html')


@app.route('/sell', methods=['POST', 'GET'])
def sales():
    sales = SalesModel.query.all()
    if request.method == 'POST':
        quantity = request.form['Quantity']
        inventoryId = request.form['InventoryId']

        sales = SalesModel(Quantity=quantity, InventoryId=inventoryId)
        sales.create_record()
        InventoryModel.update_inventory(int(inventoryId), int(quantity))

    return redirect(url_for('inventory'))

    return redirect(url_for('inventory'))


@app.route('/view_sales/<int:id>',methods = ['GET'])
def view_sales(id):
    inventory = InventoryModel.get_inventory_by_id(id)

    #print(inventory.sale)
    #print(type(inve))

    sale_of_product = inventory.sale

    return render_template('inventory.html',s_o_p=sale_of_product)


if __name__ == '__main__':
    app.run()
