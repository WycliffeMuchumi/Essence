from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from configs.config import Development, Production
import pygal

app = Flask(__name__)

# configs

app.config.from_object(Production)

# sqlAlchemy instance

db = SQLAlchemy(app)

from models import *


# create table before any request is done

@app.before_first_request
def create_table():
    db.create_all()
    # db.drop_all()


@app.route('/')
def home():
    pie_chart = pygal.Pie()
    pie_chart.title = 'Sales and products done in the year 2019 (in %)'
    pie_chart.add('product', InventoryModel.getTypeCount("product"))
    pie_chart.add('service', InventoryModel.getTypeCount("service"))
    pie_type = pie_chart.render_data_uri()
    return render_template('index.html', pie_type=pie_type)


@app.route('/about')
def about():
    return render_template('about.html')


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
        product_one = InventoryModel(productname=pn, producttype=pt, serialnumber=sn, buyingprice=bp, sellingprice=sp, stock=s, reorderpoint=rp)
        product_one.create_record()

        return redirect(url_for('inventory'))

        return render_template('inventory.html')


@app.route('/sell', methods=['POST', 'GET'])
def sales():
    sales = SalesModel.query.all()
    if request.method == 'POST':
        quantity = request.form['quantity']
        inventoryid = request.form['inventoryid']

        sale = SalesModel(quantity=quantity, inventoryid=inventoryid)
        sale.create_record()
        InventoryModel.update_stock(int(inventoryid), int(quantity))

    return redirect(url_for('inventory'))



@app.route('/view_sales/<int:id>',methods = ['GET'])
def view_sales(id):
    inventory = InventoryModel.get_inventory_by_id(id)

    #print(inventory.sale)
    #print(type(inve))

    sale_of_product = inventory.sale

    return render_template('sales.html',s_o_p=sale_of_product)




@app.route('/contacts')
def contacts():
    return render_template('contacts.html')






if __name__ == '__main__':
    app.run()
