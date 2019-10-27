from main import db

class InventoryModel(db.Model):
    __tablename__ = 'inventories'
    #columns(db.column converts id,firtsname into columns in the database)
    id = db.Column(db.Integer,primary_key=True)
    ProductName = db.Column(db.String(45), nullable=False)
    ProductType = db.Column(db.String(45), nullable=False)
    SerialNumber = db.Column(db.Integer, nullable=False,unique=True)
    BuyingPrice = db.Column(db.Integer, nullable=False)
    SellingPrice = db.Column(db.Integer, nullable=False)
    Stock = db.Column(db.Integer,nullable=False)
    ReorderPoint = db.Column(db.Integer,nullable=False)
    #create
    def create_record(self):
        db.session.add(self)
        db.session.commit()


class SalesModel(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer,primary_key=True)
    InventoryId = db.Column(db.Integer,nullable=False)
    Quantity = db.Column(db.Integer,nullable=False)


    def create_record(self):
        db.session.add(self)
        db.session.commit()

