from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from configs.config import Development, Production
import pygal
import psycopg2

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


@app.route('/', methods=['GET'])
def home():
    pie_chart = pygal.Pie()
    pie_chart.title = 'Sales and products done in the year 2019 (in %)'
    pie_chart.add('product', InventoryModel.getTypeCount("product"))
    pie_chart.add('service', InventoryModel.getTypeCount("service"))
    graph_data = pie_chart.render_data_uri()

    conn = psycopg2.connect("dbname='d36lve8t356t1v' user='blufcyfuephvbf' host='ec2-176-34-184-174.eu-west-1.compute.amazonaws.com' password='f6bb9cce21036c899c21ea893eb19ef5568e2ef2c22316547c6ee5f3f149206a'")
    # conn = psycopg2.connect("dbname='Essence' user='postgres' host='localhost' password='12121994'")

    cur = conn.cursor()
    cur.execute("""SELECT(sum(i.buyingprice * s.quantity)) as subtotal,(EXTRACT(MONTH FROM s.time_created)) as sales_month
from sales as s
join inventories as i on s.inventoryid=i.id
GROUP BY sales_month
ORDER BY sales_month""")
    rows = cur.fetchall()

    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    y = []
    for row in rows:
        # x.append(row[1])
        y.append(row[0])

    line = pygal.Line()
    line.title = '%Sales and products done in the year 2019.'
    line.x_labels = map(str, x)
    line.add('SubTotal', y)
    line_data = line.render_data_uri()

    linec = pygal.Bar()
    linec.title = '%%Sales and products done in the year 2019.'
    linec.x_labels = map(str, x)
    linec.add('SubTotal', y)
    linec = linec.render_data_uri()

    return render_template('index.html', graph_data=graph_data, line_data=line_data, linec=linec)


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
        productname = request.form['product_name']
        producttype = request.form['product_type']
        serialnumber = request.form['serial_no']
        buyingprice = request.form['buying_price']
        sellingprice = request.form['selling_price']
        stock = request.form['stock']
        reorderpoint = request.form['reorder_point']
        print(productname)
        print(producttype)
        print(serialnumber)
        print(sellingprice)
        print(stock)
        print(reorderpoint)
        product_one = InventoryModel(productname=productname, producttype=producttype, serialnumber=serialnumber,
                                     buyingprice=buyingprice, sellingprice=sellingprice,
                                     stock=stock, reorderpoint=reorderpoint)
        product_one.create_record()

        return redirect(url_for('inventory'))

        return render_template('inventory.html')


# this route edits an inventory


@app.route('/inventory/edit/<int:id>', methods=['POST'])
def edit_inventory(id):
    if request.method == 'POST':
        productname = request.form['product_name']
        producttype = request.form['product_type']
        serialnumber = request.form['serial_no']
        buyingprice = request.form['buying_price']
        sellingprice = request.form['selling_price']
        stock = request.form['stock']
        reorderpoint = request.form['reorder_point']

        update = InventoryModel.edit_inventory_by_id(id=id, productname=productname, producttype=producttype,
                                                     serialnumber=serialnumber, buyingprice=buyingprice,
                                                     sellingprice=sellingprice, stock=stock, reorderpoint=reorderpoint)

        if update:
            flash('successfully updated', 'success')
            return redirect(url_for('inventory'))
        else:
            flash('update unsuccessful', 'danger')
            return redirect(url_for('inventory'))


# the  route below deletes an inventory


@app.route('/inventory/delete/<int:id>', methods=['POST'])
def delete_inventory(id):
        delete = InventoryModel.delete_by_id(id)
        if delete:
            flash('inventory successfully delete', 'success')
            return redirect(url_for('inventory'))
        else:
            flash('This inventory has already been reimbursed', 'danger')
            return redirect(url_for('inventory'))


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


@app.route('/view_sales/<int:id>', methods=['GET'])
def view_sales(id):
    inventory = InventoryModel.get_inventory_by_id(id)

    # print(inventory.sale)
    # print(type(inve))

    sale_of_product = inventory.sale

    return render_template('sales.html', s_o_p=sale_of_product)


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run()
