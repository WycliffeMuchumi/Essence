#importing the db object from main.py file
from main import db
from datetime import datetime
from sqlalchemy.sql import func


class InventoryModel(db.Model):
    __tablename__ = 'inventories'
    # columns(db.column converts id,firtsname into columns in the database)
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(45), nullable=False)
    producttype = db.Column(db.String(45), nullable=False)
    serialnumber = db.Column(db.Integer, nullable=False, unique=True)
    buyingprice = db.Column(db.Integer, nullable=False)
    sellingprice = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    reorderpoint = db.Column(db.Integer, nullable=False)
    sale = db.relationship('SalesModel', backref='inventory', lazy=True)

    # create
    def create_record(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_inventory_by_id(cls, id):
        return InventoryModel.query.filter_by(id=id).first()


    # we first need to fetch the stock to be updated,update stock and pass the id and quantity
    @classmethod
    def update_stock(cls, id, quantity):
        record = InventoryModel.query.filter_by(id=id).first()
        if record:
            record.stock = record.stock - quantity
            db.session.commit()
            return True


    @classmethod
    def getTypeCount(cls,name):
        record = cls.query.filter_by(producttype=name).count()
        return record

    #edit
    @classmethod
    def edit_inventory_by_id(cls,id,productname=productname,producttype=producttype, serialnumber=serialnumber, buyingprice=buyingprice, sellingprice=sellingprice, stock=stock, reorderpoint=reorderpoint):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.productname = productname
            record.producttype=producttype
            record.serialnumber=serialnumber
            record.buyingprice=buyingprice
            record.sellingprice=sellingprice
            record.stock=stock
            record.reorderpoint=reorderpoint
            db.session.commit()
            return True
        else:
            return False

    #delete
    @classmethod
    def delete_by_id(cls,id):
        record=cls.query.filter_by(id=id)
        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False




class SalesModel(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    inventoryid = db.Column(db.Integer, db.ForeignKey('inventories.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)


    def create_record(self):
        db.session.add(self)
        db.session.commit()
